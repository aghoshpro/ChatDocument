from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
print ("Updated directory:" , os.getcwd())

loader = TextLoader(file_path="data/sample_docs/sample.txt")
docs = loader.load()
print(docs)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=24)
documents = text_splitter.split_documents(documents=docs)
print("\n\n")
print(documents)
