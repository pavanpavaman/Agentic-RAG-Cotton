"""
FastAPI Backend for Cotton Advisory RAG System
Provides REST API endpoints for the React frontend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import traceback

import google.generativeai as genai
USING_NEW_API = False

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Cotton Advisory API",
    description="RAG-powered API for cotton pest and disease management",
    version="1.0.0"
)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
embedder = None
index = None
texts = None
metadatas = None
model = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[Dict]] = None  # Conversation history for context

class ChatResponse(BaseModel):
    answer: str
    success: bool
    sources: Optional[List[Dict]] = None

class SystemStatus(BaseModel):
    status: str
    message: str
    model_loaded: bool
    index_loaded: bool
    chunks_count: int

def initialize_system():
    """Initialize all RAG components"""
    global embedder, index, texts, metadatas, model
    
    try:
        # Load API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        api_key = api_key.strip()
        if not api_key.startswith('AIza'):
            raise ValueError("Invalid API key format")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Load FAISS index and chunks
        if not os.path.exists('chunks.pkl'):
            raise FileNotFoundError("chunks.pkl not found")
        if not os.path.exists('faiss_index.bin'):
            raise FileNotFoundError("faiss_index.bin not found")
        
        with open('chunks.pkl', 'rb') as f:
            chunk_data = pickle.load(f)
            texts = chunk_data['texts']
            metadatas = chunk_data['metadatas']
        
        index = faiss.read_index('faiss_index.bin')
        embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        
        print("✅ System initialized successfully!")
        print(f"📊 Loaded {len(texts)} chunks")
        print(f"🤖 Using {'new google.genai' if USING_NEW_API else 'legacy google.generativeai'}")
        return True
        
    except Exception as e:
        print(f"❌ Initialization Error: {str(e)}")
        print(traceback.format_exc())
        return False

def retrieve(query: str, k: int = 5) -> List[Dict]:
    """Retrieve relevant chunks"""
    try:
        if embedder is None or index is None:
            raise RuntimeError("System not initialized")
        
        query_emb = embedder.encode([query], convert_to_numpy=True)
        D, I = index.search(query_emb, k)
        
        results = []
        for idx_pos, idx in enumerate(I[0]):
            if idx < len(texts):
                results.append({
                    'text': texts[idx],
                    'metadata': metadatas[idx],
                    'distance': float(D[0][idx_pos])
                })
        
        return results
    except Exception as e:
        print(f"Retrieval error: {e}")
        raise

def format_context_with_citations(results: List[Dict]) -> str:
    """Format retrieved context"""
    context = ""
    for r in results:
        page = r['metadata'].get('page_label', r['metadata'].get('page', '?'))
        context += f"[Source p.{page}] {r['text']}\n\n"
    return context

def answer_question(query: str, conversation_context: Optional[List[Dict]] = None) -> tuple[str, bool, List[Dict]]:
    """Generate answer using RAG with conversation context"""
    try:
        if not query or not query.strip():
            return "⚠️ Please enter a question.", False, []
        
        # Retrieve context
        retrieved = retrieve(query, k=5)
        if not retrieved:
            return "⚠️ No relevant information found.", False, []
        
        context = format_context_with_citations(retrieved)
        
        # Build conversation history context
        conversation_history = ""
        if conversation_context and len(conversation_context) > 0:
            conversation_history = "\n\nPrevious conversation:\n"
            for msg in conversation_context[-3:]:  # Use last 3 messages for context
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                conversation_history += f"{role.upper()}: {content}\n"
        
        # Create prompt with conversation context
        prompt = f"""You are a Cotton Pest and Disease Management expert assistant. Answer the following question using the provided context from the ICAR-CICR Advisory document.
{conversation_history}
Guidelines:
- Provide accurate, actionable information for cotton farmers
- Cite sources using [Source p.X] format for every fact
- If the context doesn't contain the answer, clearly state that
- Be concise but comprehensive
- Use bullet points for multiple items
- Focus on practical recommendations
- Consider the conversation history to provide contextually relevant answers

Context:
{context}

Question: {query}

Answer:"""
        
        # Get response
        if model is None:
            raise RuntimeError("Model not initialized")
        
        response = model.generate_content(prompt)
        answer = response.text
        
        if not answer or len(answer.strip()) < 10:
            raise ValueError("Generated answer too short")
        
        # Extract sources
        sources = [{
            'page': r['metadata'].get('page', '?'),
            'text': r['text'][:200] + '...'
        } for r in retrieved[:3]]
        
        return answer, True, sources
        
    except Exception as e:
        error_type = type(e).__name__
        error_str = str(e)
        print(f"❌ Error: {error_type} - {error_str}")
        
        # Provide user-friendly error messages
        if "404" in error_str or "not found" in error_str.lower():
            user_msg = "⚠️ The AI service is temporarily unavailable. Our team has been notified. Please try again in a few moments."
        elif "quota" in error_str.lower() or "rate limit" in error_str.lower():
            user_msg = "⏳ Service is currently busy. Please wait a moment and try again."
        elif "timeout" in error_str.lower():
            user_msg = "⏱️ Request timed out. Please try a shorter question or try again."
        elif "api key" in error_str.lower():
            user_msg = "🔑 Service configuration issue. Please contact support."
        else:
            user_msg = "❌ Unable to process your request right now. Please try rephrasing your question."
        
        return user_msg, False, []

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    print("🚀 Starting Cotton Advisory API...")
    success = initialize_system()
    if not success:
        print("⚠️ Warning: System initialization failed. Some features may not work.")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Cotton Advisory API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/status", response_model=SystemStatus)
async def get_status():
    """Get system status"""
    return SystemStatus(
        status="healthy" if model is not None else "unhealthy",
        message="System operational" if model is not None else "System not initialized",
        model_loaded=model is not None,
        index_loaded=index is not None,
        chunks_count=len(texts) if texts is not None else 0
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with conversation context support"""
    try:
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="System not initialized. Please check server logs."
            )
        
        answer, success, sources = answer_question(request.message, request.context)
        
        return ChatResponse(
            answer=answer,
            success=success,
            sources=sources if sources else None
        )
    
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/examples")
async def get_examples():
    """Get example questions"""
    return {
        "examples": [
            "What are the main pests affecting cotton crops?",
            "How to control pink bollworm in cotton?",
            "What is the recommended dosage for whitefly control?",
            "What preventive measures can reduce pest infestation?",
            "What are the symptoms of cotton leaf curl disease?",
            "How to identify early signs of pest infestation?",
            "What biological control methods are effective?",
            "What are the best agricultural practices?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
