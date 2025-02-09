import streamlit as st
from components.upload import handle_file_upload
from components.chat import display_chat_interface
from utils.helpers import setup_logging

logger = setup_logging()

def main():
    st.set_page_config(
        page_title="ChatDocument",
        page_icon="💬",
        layout="wide"
    )

    st.title("📚 ChatDocument")
    st.subheader("Local RAG aoo made with LangChain + Ollama")
    
    # Sidebar with file upload
    with st.sidebar:
        st.title("Upload Document")
        documents = handle_file_upload()
        
        if documents:
            st.success(f"Document processed: {len(documents)} chunks created")
    
    # Main chat interface
    display_chat_interface(documents)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please try again.")
