from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate

def get_llm():
    """Initialize and return Ollama LLM"""
    return Ollama(model="llama3.2")

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
