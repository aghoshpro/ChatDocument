# type: ignore
import streamlit as st
from typing import Optional, List, Dict
from langchain_core.documents import Document
from core.llm import get_llm_chain
from core.embeddings import get_vector_store
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from io import StringIO
import random
import time

def initialize_chat_session():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

def display_chat_interface(documents: Optional[List[Document]] = None):
    """Display chat interface and handle interactions"""
    initialize_chat_session()

    # Create two columns - one for document view and one for chat
    doc_col, chat_col = st.columns([1, 1])

    # Document viewer column
    with doc_col:
        st.subheader("Doc Information")
        doc_container = st.container(height=600)
        with doc_container:
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
                    # Download stopwords if not already downloaded
                    try:
                        nltk.data.find('corpora/stopwords')
                    except LookupError:
                        nltk.download('stopwords')

                    # Combine all document chunks
                    text = " ".join([doc.page_content for doc in documents])

                    # Removing stopwords and generating wordcloud
                    stop_words = set(stopwords.words('english'))
                    my_stopwords = [" ","https", "cdn", "None", "1280x720", "services", "http" "www", "www.", "com", "org", "net", "int", "gov", "edu", "mil", "biz", "info", "name", "pro", "aero", "co", "STS"]
                    stop_words.update(my_stopwords)
                    stop_words = set(stop_words)
                    wordcloud = WordCloud(width=800,
                                        height=540,
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
                    if 'geojson_str' in st.session_state:
                        geojson_str = st.session_state.geojson_str
                        gdf = gpd.read_file(StringIO(geojson_str))
                        non_geometry_cols = [col for col in gdf.columns if col != 'geometry']
                        # Compute bounding box
                        bounds = gdf.total_bounds
                        minx, miny, maxx, maxy = bounds
                        # Generate Folium map
                        m = folium.Map(location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=8)
                        m.fit_bounds([[miny, minx], [maxy, maxx]])  # Set map bounds to match GeoDataFrame
                        folium.GeoJson(gdf).add_to(m)  # Ensure GeoJSON is in WGS 84
                        # Add GeoJSON to map with hover functionality
                        folium.GeoJson(
                            data=gdf.to_json(),
                            style_function=lambda x: {
                                'fillColor': '#ffaf00',
                                'color': '#000000',
                                'weight': 1,
                                'fillOpacity': 0.5
                            },
                            tooltip=folium.GeoJsonTooltip(
                                fields=non_geometry_cols[:5],  # Show first 5 properties on hover
                                aliases=non_geometry_cols[:5],
                                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                            )
                        ).add_to(m)

                        # Display the map using streamlit-folium
                        folium_static(m, width=600, height=500)
                    else:
                        st.info("No geographic data found in the document")
            else:
                st.info("Upload a document to see its content here")

    # Chat column
    with chat_col:
        st.subheader("Let's Chat 🤖")
        
        # Input for user's name
        if not st.session_state.user_name:
            st.session_state.user_name = st.text_input("Say your name, human")

        # Container for chat messages
        chat_container = st.container(height=545)
        
        # Input field at the bottom
        prompt = st.chat_input(f"So, it's {st.session_state.user_name} huh, feed me your documents...")
        
        # Display chat history in the container
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    if message["role"] == "user":
                        st.markdown(f"{st.session_state.user_name}: {message['content']}")
                    else:
                        st.markdown(message["content"])
            
            if prompt:
                # Add user message to chat history
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })
                with st.chat_message("user"):
                    st.markdown(f":red[{st.session_state.user_name}] - {prompt}")

                # Generate response
                with st.chat_message("assistant"):
                    if documents:
                        try:
                            think = ["I am thinking ⏳", "Shh.. magic is happening 🔮", "Thinking, wanna tea ? ☕", "To be or not to be, that's the question 🎭 or is it 🤔?", "Red pill 🔴 or Blue pill 🔵, Neo? "]
                            with st.spinner(f":grey[{random.choice(think)}]"):
                                # Start timer
                                start_time = time.time()
                                
                                # Get existing vector store from session state or create new one
                                vector_store = st.session_state.get('vector_store') or get_vector_store(documents)
                                chain = get_llm_chain(vector_store)
                                response = chain.invoke(prompt)

                                # List of quirky responses
                                quirky_responses = [
                                    "Phew! That was a brain workout! 🧠💪",
                                    "I hope that tickled your neurons! 🧠✨",
                                    "Give me some credit! 🤔",
                                    "I feel like a supercomputer now! 💻🚀",
                                    "That was a mental marathon! 🏃‍♂️🧠",
                                    "I think I just leveled up! 🎮🧠",
                                    "That was a real synapse sizzler! 🔥🧠"
                                ]

                                # Select a random quirky response
                                quirky_response = f":rainbow[{response}]\n\n{random.choice(quirky_responses)}"
                                
                                # Calculate elapsed time
                                elapsed_time = time.time() - start_time
                                
                                # Add timing information to the response
                                response_with_time = f"{quirky_response} |  󠀠 󠀠󠀠󠀠󠀠󠀠:stopwatch: _{elapsed_time:.2f} sec_"

                                # response_with_time = f"{quirky_response} | 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠 󠀠󠀠󠀠󠀠󠀠 󠀠 󠀠 󠀠 󠀠(:stopwatch: _{elapsed_time:.2f} sec_)"
                                
                                # Typing effect
                                placeholder = st.empty()
                                typed_response = ""
                                for char in response_with_time:
                                    typed_response += char
                                    placeholder.markdown(typed_response, unsafe_allow_html=True)
                                    time.sleep(0.001)  # Adjust typing speed here

                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response_with_time
                                })
                        except Exception as e:
                            error_msg = f"Oops! My circuits got tangled: {str(e)}"
                            st.error(error_msg)
                    else:
                        st.markdown("Seriously! Come on, upload a document first.")
