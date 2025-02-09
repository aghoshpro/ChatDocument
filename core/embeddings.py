from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

def get_embeddings():
    """Initialize and return Ollama embeddings"""
    return OllamaEmbeddings(model="llama3.2")

def get_vector_store(documents):
    """Initialize and return Chroma vector store"""
    embeddings = get_embeddings()
    
    # Create vector store directory if it doesn't exist
    vector_store_path = "data/vector_store"
    os.makedirs(vector_store_path, exist_ok=True)
    
    # Create or load vector store
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=vector_store_path
    )
    
    return vector_store
