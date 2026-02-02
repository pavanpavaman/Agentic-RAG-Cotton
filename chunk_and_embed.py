from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load PDF
doc_path = r"E:\cotton_rag\document\ICAR-CICR_Advisory Pest and Disease Management 2024.pdf"
loader = PyPDFLoader(doc_path)
documents = loader.load()

# Chunk documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
)
chunks = text_splitter.create_documents([doc.page_content for doc in documents],
                                         metadatas=[doc.metadata for doc in documents])

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings
texts = [chunk.page_content for chunk in chunks]
metadatas = [chunk.metadata for chunk in chunks]
embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# Save embeddings and metadata for FAISS
with open('chunks.pkl', 'wb') as f:
    pickle.dump({'texts': texts, 'metadatas': metadatas}, f)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, 'faiss_index.bin')

print(f"Stored {len(texts)} chunks and FAISS index.")
