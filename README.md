# ChatDocument

<img src="./assets/chatoutput.gif" alt="Streamlit Web App" width="100%">

Local Retrieval Augmented Generation (RAG) application that allows you to chat with your documents such as any document such as `.txt`, `.pdf`, `.md`, `.docx`, `.doc`, `.json` (including `.geojson`) using Ollama LLMs and LangChain via a Streamlit Web UI for Q&A interaction.

## 📚 RAG System Architecture

 <img src="./assets/rag.png" alt="Streamlit Web App" width="100%">

## 📂 Project Structure

```
.
├── .streamlit/
│   └── config.toml       # Streamlit configuration (OPTIONAL)
├── assets/
│   └── ui.png            # Streamlit UI image
├── components/
│   ├── __init__.py
│   ├── chat.py           # Chat interface implementation
│   └── upload.py         # Document upload handling
├── core/
│   ├── __init__.py
│   ├── embeddings.py     # Vector embeddings configuration
│   └── llm.py            # Language model setup
├── data/
│   ├── vector_store/     # To store vector embeddings in chromadb
│   └── sample_docs/      # Sample documents for testing
├── utils/
│   ├── __init__.py
│   └── helpers.py        # Utility functions
└── main.py               # Application entry point
```

## ✨ Features
- 🔒 Complete local processing - no data leaves your machine
- 📄 Multi document (`.txt`, `.pdf`, `.md`, `.docx`, `.doc`, `.json`) processing with intelligent chunking
- 🧠 Multi-query retrieval for better context understanding
- 🎯 Advanced RAG implementation using LangChain
- 🖥️ Clean Streamlit interface
- 📓 Jupyter notebook for experimentation

## 🚀 Getting Started

### 1. **Install Ollama**

- Visit [Ollama's website](https://ollama.com) to download Ollama and install

- Open `cmd` or `terminal` and run `ollama`

- Install initial models (local):

  ```bash
  ollama pull llama3.2  
  ollama pull deepseek-r1:8b
  ollama pull [your preferred model name]
  ```

- Chat with the model,

  ```bash
  ollama run llama3.2   # or your preferred model
  ```

- For embeddings pull the following,

  ```bash
  ollama pull `mxbai-embed-large` # or your preferred model such as `nomic-embed-text`
  ```

- Check the list of locally available ollama models:
  ```bash
  ollama list
  ```
### 2. **Clone Repository**

- Open `cmd` or `terminal` to clone repository in your preferred file location

  ```bash
  git clone https://github.com/aghoshpro/ChatDocument.git
  ```

### 3. **Set Up Local Environment**

- Create a virtual environment `myvenv` and activate it:

  ```bash
  python -m venv myvenv
  ```

  ```bash
  .\myvenv\Scripts\activate    # On Windows

  # ---------------------- OR ---------------------- #

  source myvenv/bin/activate  # On Linux or Mac
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- 🧪 Experiment with code if you want
  ```sh
  jupyter notebook
  ```
## 🎮 Run Streamlit Web App

```bash
streamlit run main.py
```
- Content View
  <img src="./assets/ui.png" alt="Streamlit Web App" width="100%">

- WordCloud View:
  <img src="./assets/ui2.png" alt="Streamlit Web App" width="100%">

## 🛠 Troubleshooting

- Ensure Ollama is running in the background
- GPU preferred if not CPU (will be slower)
- ./data/sample_docs contains few local documents for you to test
- Delete data/vector_store/ that holds embeddings in case delete file option failed to delete docs.

## ✨Theme Configuration

- Create `.streamlit/config.toml` with:

  ```toml
  [theme]
  primaryColor = "#FF4B4B"
  backgroundColor = "#FFFFFF"
  secondaryBackgroundColor = "#F0F2F6"
  textColor = "#262730"
  font = "sans serif"
  ```
## 🤝 Contributing
- Open issues for bugs or suggestions
- Submit pull requests

## 📑 References

### Docs

- [LangChain](https://python.langchain.com/docs/index.html)
- [Ollama](https://ollama.com/docs/index.html)
- [ChromaDB](https://www.trychroma.com/)
- [Streamlit](https://docs.streamlit.io/)
- [Folium](https://python-visualization.github.io/folium/)
- [Unstructured](https://docs.unstructured.io/platform/supported-file-types)
- [ChromaDB Tutorial Step by Step Guide](https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide)
- [ChromaDB Collections](https://docs.trychroma.com/docs/collections/create-get-delete)

### Blogs

- [Finding the Best Open Source Embedding Model for RAG](https://medium.com/timescale/finding-the-best-open-source-embedding-model-for-rag-929d1656d331)
- [Enhancing Retrieval Augmented Generation with ChromaDB and SQLite](https://medium.com/@dassandipan9080/enhancing-retrieval-augmented-generation-with-chromadb-and-sqlite-c499109f8082)
- [Implementing RAG in LangChain with Chroma](https://medium.com/@callumjmac/implementing-rag-in-langchain-with-chroma-a-step-by-step-guide-16fc21815339)
- [Build Your Own RAG and Run Them Locally](https://blog.duy.dev/build-your-own-rag-and-run-them-locally/)