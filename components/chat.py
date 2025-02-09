import streamlit as st
from typing import Optional
from langchain_core.documents import Document
from core.llm import get_llm_chain
from core.embeddings import get_vector_store

def initialize_chat_session():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_interface(documents: Optional[list[Document]] = None):
    """Display chat interface and handle interactions"""
    initialize_chat_session()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to know about the document?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            if documents:
                try:
                    vector_store = get_vector_store(documents)
                    chain = get_llm_chain(vector_store)
                    # Pass the prompt directly as a string
                    response = chain.invoke(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.markdown(response)
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
            else:
                st.markdown("Please upload a document first.")