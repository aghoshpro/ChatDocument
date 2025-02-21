# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
import ollama
import streamlit as st
import logging
logger = logging.getLogger(__name__)

def extract_model_names(models_info):
    """Extract model names from the provided models information."""
    logger.info("Extracting model names from models_info")
    try:
        if hasattr(models_info, "models"):
            model_names = tuple(model.model for model in models_info.models)
        else:
            model_names = tuple()
        logger.info(f"Extracted model names: {model_names}")
        return model_names
    except Exception as e:
        logger.error(f"Error extracting model names: {e}")
        return tuple()

def get_available_models():
    """Get list of available Ollama models"""
    try:
        models_info = ollama.list()
        model_names = extract_model_names(models_info)
        return model_names if model_names else ("llama3.2:latest",)
    except Exception as e:
        st.error(f"Error fetching models: {str(e)}")
        return ("llama3.2")

def get_llm():
    """Initialize and return Ollama LLM with selected model"""
    selected_model = st.session_state.get('selected_model', 'llama3.2')
    return OllamaLLM(model=selected_model)

def get_llm_chain(vector_store):
    """Create and return the RAG chain"""
    llm = get_llm()
    
    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    
    Answer: """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
