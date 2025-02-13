# type: ignore
import streamlit as st
from typing import Optional, Dict, Any
import tempfile
import json
import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
    JSONLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    TokenTextSplitter
)
from langchain.schema import Document
from utils.helpers import get_file_extension
import logging
import pandas as pd
import geopandas as gpd
from io import StringIO

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {
    '.txt': ('Text files', '.txt'),
    '.pdf': ('PDF files', '.pdf'),
    '.docx': ('Word documents', '.docx'),
    '.doc': ('Word documents', '.doc'),
    '.json': ('JSON files', '.json'),
    '.geojson': ('GeoJSON files', '.geojson'),
    '.csv': ('CSV files', '.csv'),
    '.md': ('Markdown files', '.md')
}

CHUNKING_STRATEGIES = {
    'recursive': 'Recursive Character (Smart)',
    'token': 'Token-based',
    'markdown': 'Markdown-aware'
}

def extract_json_content(data: dict) -> str:
    """Extract content from JSON data"""
    try:
        # Check if it's a GeoJSON file by looking for typical GeoJSON structure
        if isinstance(data, dict) and 'type' in data and 'features' in data:
            # Handle GeoJSON
            features = data.get('features', [])
            properties = [feature.get('properties', {}) for feature in features]
            return json.dumps(properties, indent=2)
        else:
            # Regular JSON handling
            return json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)
    except Exception as e:
        logger.error(f"Error extracting JSON content: {str(e)}")
        raise ValueError(f"Failed to process JSON content: {str(e)}")

def get_text_splitter(strategy: str, params: Dict[str, Any]):
    """Get appropriate text splitter based on strategy"""
    if strategy == 'recursive':
        return RecursiveCharacterTextSplitter(
            chunk_size=params['chunk_size'],
            chunk_overlap=params['chunk_overlap'],
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    elif strategy == 'token':
        return TokenTextSplitter(
            chunk_size=params['chunk_size'] // 4,  # Token-based chunks are typically shorter
            chunk_overlap=params['chunk_overlap'] // 4
        )
    elif strategy == 'markdown':
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        return MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")

def delete_vector_store():
    """Delete the vector store directory and clear related session state"""
    import shutil
    vector_store_path = "data/vector_store"
    
    # Debug: Check if the path exists
    if os.path.exists(vector_store_path):
        try:
            shutil.rmtree(vector_store_path)
            logger.info(f"Deleted vector store at {vector_store_path}")
        except Exception as e:
            logger.error(f"Failed to delete vector store: {str(e)}")
            st.error(f"Failed to delete vector store: {str(e)}")
            return

    # Clear all related session state
    for key in ['documents', 'messages']:
        if key in st.session_state:
            del st.session_state[key]
            logger.info(f"Cleared session state for key: {key}")

    st.success("Vector store and chat history deleted successfully!")

def handle_file_upload() -> Optional[list]:
    """Handle document upload and processing with advanced chunking"""
    uploaded_file = st.file_uploader(
        "",
        type=[fmt[1:] for fmt in SUPPORTED_FORMATS.keys()]
    )

    # Show supported formats in the UI
    # st.markdown("# ✅ Supported Formats")
    # formats_text = " | ".join([f"{desc[0]} (*.{ext[1:]})" for ext, desc in SUPPORTED_FORMATS.items()])
    # st.caption(f"{formats_text}")

    st.markdown("# ❌ Remove Document")
    if st.button("Delete Document", type="secondary"):
        delete_vector_store()
        st.rerun()

    # Chunking strategy configuration
    st.markdown("# 🎟 Chunking")
    with st.expander("Settings", expanded=False):
        strategy = st.selectbox(
            "Chunking Strategy",
            options=list(CHUNKING_STRATEGIES.keys()),
            format_func=lambda x: CHUNKING_STRATEGIES[x],
            help="Choose how to split your document into chunks"
        )

        # Only show size parameters for non-markdown strategies
        chunk_params = {}
        if strategy != 'markdown':
            col1, col2 = st.columns(2)
            with col1:
                chunk_params['chunk_size'] = st.slider(
                    "Chunk Size",
                    min_value=100,
                    max_value=2000,
                    value=1000,
                    step=100,
                    help="Number of characters per chunk"
                )
            with col2:
                chunk_params['chunk_overlap'] = st.slider(
                    "Chunk Overlap",
                    min_value=0,
                    max_value=500,
                    value=200,
                    step=50,
                    help="Number of overlapping characters between chunks"
                )


    if uploaded_file is not None:
        try:
            # Create a temporary file to store the uploaded content
            with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name

            # Load document based on file type
            file_extension = get_file_extension(uploaded_file.name)

            try:
                if file_extension == '.txt':
                    loader = TextLoader(file_path)
                elif file_extension == '.pdf':
                    loader = PyPDFLoader(file_path)
                elif file_extension in ['.docx', '.doc']:
                    try:
                        loader = Docx2txtLoader(file_path)
                    except Exception:
                        # Fallback to UnstructuredWordDocumentLoader if Docx2txtLoader fails
                        loader = UnstructuredWordDocumentLoader(file_path)
                elif file_extension in ['.json']:
                    with open(file_path, 'r') as f:
                        df = pd.read_json(f)
                        json_content = df.to_string()
                        # json_content = extract_json_content(json.load(f))
                        if 'dataframe' not in st.session_state:
                            st.session_state.dataframe = {}
                        st.session_state.dataframe[file_path] = df
                    documents = [Document(page_content=json_content, metadata={"source": file_path})]
                    return documents
                elif file_extension in ['.geojson']:
                    with open(file_path, 'r') as f:
                        try:
                            geojson_str = uploaded_file.getvalue().decode('utf-8')
                            json_content = extract_json_content(json.loads(geojson_str))
                            documents = [Document(page_content=json_content, metadata={"source": file_path})]
                            # Save geojson_str to session state to be used in another file
                            st.session_state.geojson_str = geojson_str
                            gdf = gpd.read_file(StringIO(geojson_str))
                            if 'dataframe' not in st.session_state:
                                    st.session_state.dataframe = {}
                            st.session_state.dataframe[file_path] = gdf
                        except json.JSONDecodeError:
                            st.error("Invalid GeoJSON file. Please ensure the file is properly formatted.")
                            return None
                        except Exception as e:
                            st.error(f"Error processing GeoJSON file: {str(e)}")
                            return None
                    return documents
                elif file_extension == '.csv':
                    df = pd.read_csv(file_path)
                    # Convert DataFrame to text for vector store
                    text_content = df.to_string()
                    # Store only the source in metadata, keep DataFrame in session state
                    if 'dataframe' not in st.session_state:
                        st.session_state.dataframe = {}
                    st.session_state.dataframe[file_path] = df
                    documents = [Document(page_content=text_content, metadata={"source": file_path})]
                    return documents
                elif file_extension == '.md':
                    loader = UnstructuredMarkdownLoader(file_path)
                else:
                    st.error(f"Unsupported file type: {file_extension}")
                    return None

                documents = loader.load()

                # Get appropriate text splitter
                text_splitter = get_text_splitter(strategy, chunk_params)

                # Split documents into chunks
                chunks = text_splitter.split_documents(documents)

                if not chunks:
                    st.warning("The document appears to be empty. Please upload a document with content.")
                    return None

                # Display chunking statistics
                st.success(f"Successfully processed document into {len(chunks)} chunks")
                st.info(f"""
                Chunking Statistics:
                - Average chunk size: {sum(len(chunk.page_content) for chunk in chunks) // len(chunks)} characters
                - Number of chunks: {len(chunks)}
                - Chunking strategy: {CHUNKING_STRATEGIES[strategy]}
                """)

                return chunks

            except Exception as e:
                logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
                st.error(f"Error processing your file: {str(e)}")
                return None

        except Exception as e:
            logger.error(f"Error handling file upload: {str(e)}")
            st.error("An error occurred while uploading your file. Please try again.")
            return None

    return None