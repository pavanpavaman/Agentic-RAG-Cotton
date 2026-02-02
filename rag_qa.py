import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# For LLM, you can use OpenAI, HuggingFace, or any local model. Here, we use OpenAI as an example.
import google.generativeai as genai

# Load FAISS index and chunk metadata
with open('chunks.pkl', 'rb') as f:
    chunk_data = pickle.load(f)
    texts = chunk_data['texts']
    metadatas = chunk_data['metadatas']

index = faiss.read_index('faiss_index.bin')
embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

# Simple retriever function
def retrieve(query: str, k: int = 5) -> List[Dict]:
    query_emb = embedder.encode([query], convert_to_numpy=True)
    D, I = index.search(query_emb, k)
    results = []
    for idx in I[0]:
        results.append({
            'text': texts[idx],
            'metadata': metadatas[idx]
        })
    return results

# Format context for LLM prompt with citations
def format_context_with_citations(results: List[Dict]) -> str:
    context = ""
    for i, r in enumerate(results):
        page = r['metadata'].get('page_label', r['metadata'].get('page', '?'))
        context += f"[Source p.{page}] {r['text']}\n"
    return context


# Main RAG QA function
def answer_question(query: str, api_key: str = None) -> str:
    if api_key is None:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env file")
    
    # Strip whitespace and validate API key format
    api_key = api_key.strip()
    if not api_key.startswith('AIza'):
        raise ValueError(f"Invalid API key format. Key should start with 'AIza', got: '{api_key[:10]}...'")
    
    retrieved = retrieve(query, k=5)
    context = format_context_with_citations(retrieved)
    prompt = (
        "Answer the following question using ONLY the provided context. "
        "For every fact, cite the source page in the format [Source p.X].\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer: "
    )
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    user_query = input("Enter your question: ")
    print("\n---\n")
    print(answer_question(user_query))
