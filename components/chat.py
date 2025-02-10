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

    # Create two columns - one for document view and one for chat
    doc_col, chat_col = st.columns([1, 1])

    # Document viewer column
    with doc_col:
        st.subheader("Doc Information")
        if documents:
            tabs = st.tabs(["Content 📄", "𝒲ord Cloud 🔠", "Data View 📊", "Map View 🌎"])

            # Content Tab
            with tabs[0]:
                chunk_tabs = st.tabs(
                    [f"Chunk {i+1}" for i in range(len(documents))])
                for i, tab in enumerate(chunk_tabs):
                    with tab:
                        st.text(documents[i].page_content)

            # Word Cloud Tab
            with tabs[1]:
                import nltk
                from nltk.corpus import stopwords
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt

                # Download stopwords if not already downloaded
                try:
                    nltk.data.find('corpora/stopwords')
                except LookupError:
                    nltk.download('stopwords')

                # Combine all document chunks
                text = " ".join([doc.page_content for doc in documents])

                # Generate wordcloud
                stop_words = set(stopwords.words('english'))
                wordcloud = WordCloud(width=800,
                                      height=400,
                                      background_color='white',
                                      stopwords=stop_words).generate(text)

                # Display wordcloud
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)

            # Data View Tab
            with tabs[2]:
                if 'dataframe' in st.session_state:
                    for doc in documents:
                        source = doc.metadata.get('source', '')
                        if source in st.session_state.dataframe:
                            st.dataframe(st.session_state.dataframe[source])
                        else:
                            st.info("No tabular data available for this document")
                else:
                    st.info("No tabular data available")

            # Map View Tab
            with tabs[3]:
                for doc in documents:
                    if 'dataframe' in doc.metadata:
                        df = doc.metadata['dataframe']
                        if 'latitude' in df.columns and 'longitude' in df.columns:
                            st.map(df)
                        else:
                            st.info("No geographic data found in the document")
                    else:
                        st.info(
                            "No geographic data available for this document")
        else:
            st.info("Upload a document to see its content here")

    # Chat column
    with chat_col:
        st.subheader("Let's Chat 🤖")
        # Container for chat messages
        chat_container = st.container()
        
        # Input field at the bottom
        prompt = st.chat_input("What would you like to know about the document?")
        
        # Display chat history in the container
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            if prompt:
                # Add user message to chat history
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate response
                with st.chat_message("assistant"):
                    if documents:
                        try:
                            with st.spinner("I am thinking...⏳"):
                                vector_store = get_vector_store(documents)
                                chain = get_llm_chain(vector_store)
                                response = chain.invoke(prompt)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response
                                })
                                st.markdown(response)
                        except Exception as e:
                            error_msg = f"Error generating response: {str(e)}"
                            st.error(error_msg)
                    else:
                        st.markdown("Please upload a document first.")
