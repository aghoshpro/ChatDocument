# type: ignore
import os
import streamlit as st
import ollama
from core.llm import extract_model_names
from components.upload import handle_file_upload
from components.chat import display_chat_interface
from utils.helpers import setup_logging
from core.embeddings import get_vector_store
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
logger = setup_logging()

def main():
    st.set_page_config(
        page_title="ChatDocument",
        page_icon="📚",
        layout="wide"
    )
    st.title("📚 :rainbow[ChatDocument]")
    # Sidebar
    with st.sidebar:
        st.title("🤖 Select LLM Model")
        # Model selection
        try:
            models_info = ollama.list()
            available_models = extract_model_names(models_info)
            if not available_models:
                available_models = ("llama3.2:latest",)
                st.warning("No models found. using llama3.2:latest as default")
            
            # Filter out embedding models from available_models
            filtered_models = [model for model in available_models if not model.endswith('-embed-') and not 'embed' in model]
            
            current_index = 0
            if "selected_model" in st.session_state and st.session_state.selected_model in filtered_models:
                current_index = filtered_models.index(st.session_state.selected_model)
            
            selected_model = st.selectbox(
                "",
                options=filtered_models,
                index=current_index
            )
            st.session_state.selected_model = selected_model
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            st.session_state.selected_model = "llama3.2:latest"
        st.title("📗 Upload Document")
        documents = handle_file_upload()
        
        if documents:
            st.session_state['documents'] = documents
            # Create vector store with force_refresh=True for new documents
            vector_store = get_vector_store(documents, force_refresh=True)
            st.session_state['vector_store'] = vector_store
            st.success(f"Document processed: {len(documents)} chunks created")
        elif 'documents' in st.session_state:
            documents = st.session_state['documents']
    
    # Main chat interface
    display_chat_interface(documents)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please try again.")
