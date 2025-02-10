from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
import os
import logging
logger = logging.getLogger(__name__)

def get_vector_store(documents=None):
    """Get or create vector store"""
    persist_directory = "data/vector_store"
    
    # Ensure the directory exists
    os.makedirs(persist_directory, exist_ok=True)
    
    # Initialize embeddings
    embeddings = OllamaEmbeddings(model="llama3.2")
    
    # Initialize ChromaDB client with explicit settings
    chroma_client = chromadb.PersistentClient(
        path=persist_directory,
        settings=chromadb.Settings(
            allow_reset=True,
            is_persistent=True
        )
    )
    
    # Create or load vector store
    if documents:
        return Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_directory,
            client=chroma_client
        )
    else:
        return Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
            client=chroma_client
        )
