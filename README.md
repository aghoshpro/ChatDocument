# ChatDocument

System requirements:

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) for local LLM inference
- `jq` for JSON processing (can be installed via package manager)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd local-rag-chatbot
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required Python packages:

```bash
pip install langchain langchain-core langchain-community langchain-ollama streamlit python-docx chromadb docx2txt pypdf
```

4. Install system dependencies:

   - **Ollama**:
     - Visit [https://ollama.ai/](https://ollama.ai/)
     - Follow the installation instructions for your operating system
   - **jq** (for JSON processing):
     - Linux: `sudo apt-get install jq`
     - macOS: `brew install jq`
     - Windows: Download from [stedolan.github.io/jq](https://stedolan.github.io/jq/)

5. Pull the Llama2 model:

```bash
ollama pull llama2
```

## Project Structure

```
.
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── components/
│   ├── __init__.py
│   ├── chat.py           # Chat interface implementation
│   └── upload.py         # Document upload handling
├── core/
│   ├── __init__.py
│   ├── embeddings.py     # Vector embeddings configuration
│   └── llm.py           # Language model setup
├── data/
│   └── vector_store/     # Chroma vector store data
├── utils/
│   ├── __init__.py
│   └── helpers.py        # Utility functions
└── main.py              # Application entry point
```

## Configuration

1. Create `.streamlit/config.toml` with:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## Usage

1. Ensure Ollama is running in the background:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags
```

2. Start the application:

```bash
streamlit run main.py
```
