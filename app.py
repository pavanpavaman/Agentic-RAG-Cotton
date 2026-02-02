"""
Cotton Advisory RAG Chat Interface
A professional ChatGPT-like interface for querying cotton pest and disease management information
"""
import gradio as gr
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import traceback

# Load environment variables
load_dotenv()

# Global variables for caching
embedder = None
index = None
texts = None
metadatas = None
model = None

class CottonRAGSystem:
    """Professional RAG system with error handling and caching"""
    
    def __init__(self):
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize all components with proper error handling"""
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
                raise FileNotFoundError("chunks.pkl not found. Please run chunk_and_embed.py first")
            if not os.path.exists('faiss_index.bin'):
                raise FileNotFoundError("faiss_index.bin not found. Please run chunk_and_embed.py first")
            
            with open('chunks.pkl', 'rb') as f:
                chunk_data = pickle.load(f)
                texts = chunk_data['texts']
                metadatas = chunk_data['metadatas']
            
            index = faiss.read_index('faiss_index.bin')
            
            # Load embedding model (CPU only for compatibility)
            embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            
            return True, "✅ System initialized successfully!"
            
        except Exception as e:
            error_msg = f"❌ Initialization Error: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            return False, error_msg
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant chunks with error handling"""
        try:
            if embedder is None or index is None:
                raise RuntimeError("System not initialized properly")
            
            query_emb = embedder.encode([query], convert_to_numpy=True)
            D, I = index.search(query_emb, k)
            
            results = []
            for idx in I[0]:
                if idx < len(texts):  # Validate index
                    results.append({
                        'text': texts[idx],
                        'metadata': metadatas[idx],
                        'distance': float(D[0][len(results)])
                    })
            
            return results
        except Exception as e:
            print(f"Retrieval error: {e}")
            raise
    
    def format_context_with_citations(self, results: List[Dict]) -> str:
        """Format retrieved context with page citations"""
        context = ""
        for i, r in enumerate(results, 1):
            page = r['metadata'].get('page_label', r['metadata'].get('page', '?'))
            context += f"[Source p.{page}] {r['text']}\n\n"
        return context
    
    def answer_question(self, query: str, max_retries: int = 3) -> Tuple[str, bool]:
        """
        Answer a question with retry logic and error handling
        Returns: (answer, success)
        """
        if not query or not query.strip():
            return "⚠️ Please enter a question about cotton pest and disease management.", False
        
        for attempt in range(max_retries):
            try:
                # Retrieve relevant context
                retrieved = self.retrieve(query, k=5)
                
                if not retrieved:
                    return "⚠️ No relevant information found in the knowledge base. Please try rephrasing your question.", False
                
                context = self.format_context_with_citations(retrieved)
                
                # Create prompt
                prompt = f"""You are a Cotton Pest and Disease Management expert assistant. Answer the following question using ONLY the provided context from the ICAR-CICR Advisory document.

Guidelines:
- Provide accurate, actionable information for cotton farmers
- Cite sources using [Source p.X] format for every fact
- If the context doesn't contain the answer, clearly state that
- Be concise but comprehensive
- Use bullet points for multiple items
- Focus on practical recommendations

Context:
{context}

Question: {query}

Answer:"""
                
                # Get response from Gemini
                if model is None:
                    raise RuntimeError("Gemini model not initialized")
                
                response = model.generate_content(prompt)
                answer = response.text
                
                # Validate answer
                if not answer or len(answer.strip()) < 10:
                    raise ValueError("Generated answer too short or empty")
                
                return answer, True
                
            except Exception as e:
                error_type = type(e).__name__
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    # Final attempt failed
                    error_msg = f"❌ Error: {error_type} - {str(e)}\n\n"
                    error_msg += "Please try again or contact support if the issue persists."
                    return error_msg, False
        
        return "❌ Maximum retry attempts reached. Please try again later.", False

# Initialize the RAG system
rag_system = CottonRAGSystem()

def chat_interface(message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
    """
    Chat interface function for Gradio
    Args:
        message: User's message
        history: Chat history
    Returns:
        Updated history
    """
    if not message or not message.strip():
        return history
    
    # Generate response
    answer, success = rag_system.answer_question(message)
    
    # Add to history
    history.append([message, answer])
    
    return history

def format_example_questions():
    """Return example questions as a formatted string"""
    examples = [
        "What are the main pests affecting cotton crops?",
        "How to control pink bollworm in cotton?",
        "What are the symptoms of cotton leaf curl disease?",
        "What is the recommended dosage for whitefly control?",
        "What preventive measures can reduce pest infestation?",
        "How to identify early signs of pest infestation?",
        "What biological control methods are effective for cotton pests?",
        "What are the best agricultural practices to minimize cotton diseases?"
    ]
    return examples

# Create custom CSS for ChatGPT-like appearance
custom_css = """
#main-container {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}

.header-section {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.header-title {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.header-subtitle {
    font-size: 1.2em;
    opacity: 0.95;
    margin-top: 10px;
}

.info-box {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    border-left: 4px solid #667eea;
}

.example-questions {
    background: #ffffff;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.footer {
    text-align: center;
    padding: 20px;
    color: #6c757d;
    margin-top: 30px;
    border-top: 1px solid #dee2e6;
}

/* Chat message styling */
.message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
    line-height: 1.6;
}

.user-message {
    background: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.bot-message {
    background: #f5f5f5;
    border-left: 4px solid #4caf50;
}

/* Button styling */
.primary-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
}

.primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
"""

def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(title="Cotton Advisory Chat") as demo:
        # Header
        gr.HTML("""
            <div class="header-section">
                <div class="header-title">🌱 Cotton Advisory Chat Assistant</div>
                <div class="header-subtitle">
                    Powered by ICAR-CICR | Expert Guidance on Pest & Disease Management
                </div>
            </div>
        """)
        
        # Info section
        with gr.Row():
            gr.Markdown("""
                <div class="info-box">
                    <h3>📋 About This System</h3>
                    <p>This AI assistant provides expert advice on cotton pest and disease management based on the 
                    <strong>ICAR-CICR Advisory 2024</strong>. Ask questions about:</p>
                    <ul>
                        <li>🐛 Pest identification and control (bollworms, whitefly, mealybugs, etc.)</li>
                        <li>🦠 Disease management (leaf curl, bacterial blight, wilt, etc.)</li>
                        <li>💊 Recommended pesticide dosages and application methods</li>
                        <li>🌾 Integrated pest management strategies</li>
                        <li>🛡️ Preventive measures and best practices</li>
                    </ul>
                    <p><strong>Note:</strong> All answers include source page citations for verification.</p>
                </div>
            """)
        
        # Main chat interface
        chatbot = gr.Chatbot(
            label="Chat History",
            height=500,
            show_label=True
        )
        
        with gr.Row():
            msg = gr.Textbox(
                label="Your Question",
                placeholder="Ask me anything about cotton pest and disease management...",
                lines=2,
                scale=4
            )
            submit = gr.Button("Send 📤", scale=1, variant="primary")
        
        with gr.Row():
            clear = gr.Button("🗑️ Clear Chat", scale=1)
            gr.Button("ℹ️ Help", scale=1)
        
        # Example questions
        gr.Markdown("""
            <div class="example-questions">
                <h3>💡 Example Questions</h3>
                <p>Click on any question below to try it:</p>
            </div>
        """)
        
        examples = gr.Examples(
            examples=format_example_questions(),
            inputs=msg,
            label="Click to use these example questions"
        )
        
        # System status
        with gr.Accordion("⚙️ System Status & Information", open=False):
            status = gr.Markdown("""
                ### System Information
                - **Knowledge Base**: ICAR-CICR Advisory - Pest and Disease Management 2024
                - **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
                - **Vector Database**: FAISS
                - **LLM**: Google Gemini 2.5 Flash
                - **Retrieval**: Top-5 most relevant chunks
                - **Status**: ✅ System Ready
            """)
        
        # Footer
        gr.HTML("""
            <div class="footer">
                <p><strong>🌱 Cotton Advisory RAG System</strong></p>
                <p>Built with ❤️ for Cotton Farmers | Data Source: ICAR-CICR 2024</p>
                <p style="font-size: 0.9em; color: #999;">
                    Disclaimer: This system provides advisory information based on ICAR-CICR guidelines. 
                    Always consult with local agricultural experts for specific situations.
                </p>
            </div>
        """)
        
        # Event handlers
        def respond(message, chat_history):
            if not message.strip():
                return chat_history, ""
            
            # Generate bot response
            answer, success = rag_system.answer_question(message)
            
            # Gradio 6.0 format: list of dicts with 'role' and 'content'
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": answer})
            
            return chat_history, ""
        
        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        submit.click(respond, [msg, chatbot], [chatbot, msg])
        clear.click(lambda: [], None, chatbot)
    
    return demo

if __name__ == "__main__":
    # Initialize and launch
    print("🚀 Starting Cotton Advisory Chat Assistant...")
    
    # Check system initialization
    success, message = rag_system.initialize_system()
    print(message)
    
    if success:
        demo = create_interface()
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=True
        )
    else:
        print("❌ Failed to initialize system. Please check your configuration.")
        print("Make sure you have:")
        print("1. Set GEMINI_API_KEY in .env file")
        print("2. Run chunk_and_embed.py to generate embeddings")
        print("3. Installed all required packages")
