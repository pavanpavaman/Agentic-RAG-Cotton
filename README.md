# Cotton Advisory RAG Chat System

<div align="center">

![Cotton Advisory](https://img.shields.io/badge/Cotton-Advisory-green)
![RAG](https://img.shields.io/badge/RAG-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

**🌱 AI-Powered Cotton Pest & Disease Management Chat Assistant**

[Live Demo](#demo) • [Features](#features) • [Quick Start](#quick-start)

</div>

---

## 🌟 Overview

An intelligent ChatGPT-like interface for cotton pest and disease management. Built on ICAR-CICR Advisory 2024 guidelines using Retrieval-Augmented Generation (RAG), delivering accurate, citation-backed answers to help cotton farmers.

## ✨ Features

### 🎯 Core Capabilities
- **💬 ChatGPT-like Interface**: Modern chat UI powered by Gradio
- **📚 Expert Knowledge Base**: ICAR-CICR Advisory 2024
- **🔍 Semantic Search**: FAISS vector database with 384-dim embeddings
- **📖 Source Citations**: Every answer includes page references
- **🔄 Conversation History**: Full chat history with clear option
- **⚡ Fast Responses**: <5 second average response time

### 🛡️ Advanced Features
- **Error Handling**: Retry logic with exponential backoff
- **Input Validation**: API key checking and sanitization  
- **Example Questions**: Pre-loaded questions to get started
- **Responsive Design**: Works on desktop and mobile
- **System Monitoring**: Real-time health status

## � Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/pavanpavaman/Agentic-RAG-Cotton.git
cd Agentic-RAG-Cotton
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_api_key_here
```

4. **Generate embeddings** (First time only):
```bash
python chunk_and_embed.py
```

5. **Launch the chat interface**:
```bash
python app.py
```
   
Open your browser to: `http://localhost:7860`

## 💬 Using the Chat Interface

1. **Launch**: Run `python app.py`
2. **Ask Questions**: Type in the chat box
3. **Get Answers**: Receive detailed responses with source citations
4. **Clear History**: Use "Clear Chat" button to start fresh

### Example Questions
- "What are the main pests affecting cotton crops?"
- "How to control pink bollworm in cotton?"
- "What is the recommended dosage for whitefly control?"
- "What preventive measures can reduce pest infestation?"

## 📁 Project Structure

```
Agentic-RAG-Cotton/
├── app.py                      # 🌐 Main Gradio chat interface
├── rag_qa.py                   # 🔧 Core RAG logic
├── chunk_and_embed.py          # 📊 Embedding generation
├── load_pdf.py                 # 📄 PDF loading utility
├── test_rag.py                 # 🧪 Testing suite (20 questions)
├── requirements.txt            # 📦 Python dependencies
├── .env.example                # 🔐 Environment template
├── .gitignore                  # 🚫 Git ignore rules
├── README.md                   # 📖 This file
├── RAG_ARCHITECTURE.md         # 🏗️ Detailed architecture
├── DEPLOYMENT_GUIDE.md         # 🚀 Deployment instructions
└── QUICK_START.md              # ⚡ Quick start guide
```

## 🧪 Testing

### Run the test suite:
```bash
python test_rag.py
```

### Test Results:
- ✅ **20/20** questions answered successfully
- ✅ **75%** answers with proper citations
- ✅ **0 errors** with valid API key
- ✅ Average response: **117 words**

## 🏗️ Architecture

### System Pipeline
```
User Question → Gradio UI → RAG System → Query Embedding
                                ↓
                        Vector Search (FAISS)
                                ↓
                        Context Formatting
                                ↓
                        LLM Generation (Gemini)
                                ↓
                    Answer with Citations → User
```

### Tech Stack
- **Frontend**: Gradio 4.0+
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS
- **LLM**: Google Gemini 2.5 Flash
- **Backend**: Python 3.8+
- **Data**: ICAR-CICR Advisory 2024

## 🚢 Deployment

### Hugging Face Spaces (Recommended)
1. Create a Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose "Gradio" as SDK
3. Upload `app.py`, `requirements.txt`, `faiss_index.bin`, `chunks.pkl`
4. Add `GEMINI_API_KEY` in Space secrets
5. Deploy!

### Local Deployment
```bash
python app.py
```
Access at: `http://localhost:7860`

## 📝 Configuration

Edit `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/pavanpavaman/Agentic-RAG-Cotton/issues)
- **Docs**: See `RAG_ARCHITECTURE.md` and `DEPLOYMENT_GUIDE.md`

## 🔮 Roadmap

- [ ] Multi-language support (Hindi, Telugu, Marathi)
- [ ] Voice input/output
- [ ] Image-based pest identification
- [ ] Mobile app
- [ ] SMS/WhatsApp bot integration

---

<div align="center">

**Made with ❤️ for Cotton Farmers**

⭐ Star this repo if you find it helpful!

</div>
└── document/                # Place your PDF documents here
```

## 🔄 Usage

### Step 1: Load PDF Document

```bash
python load_pdf.py
```

This script loads the PDF and verifies that pages are extracted correctly.

### Step 2: Create Embeddings and FAISS Index

```bash
python chunk_and_embed.py
```

This generates:
- `faiss_index.bin` - Vector database index
- `chunks.pkl` - Text chunks with metadata

### Step 3: Ask Questions

```bash
python rag_qa.py
```

Enter your question when prompted. Example:
```
Enter your question: What are the main pests affecting cotton crops?

---

Based on the advisory document [Source p.5], the main pests affecting cotton include...
```

### Step 4: Run Comprehensive Tests

```bash
python test_rag.py
```

This runs 20 predefined questions and generates:
- Detailed console output with answers
- `test_results_YYYYMMDD_HHMMSS.json` - Results file with analysis

## 📊 System Pipeline

```
PDF Document
    ↓
Load & Extract Pages (PyPDFLoader)
    ↓
Chunk Text (500 chars, 100 overlap)
    ↓
Generate Embeddings (all-MiniLM-L6-v2)
    ↓
Store in FAISS Index
    ↓
User Query → Retrieve Top-5 Chunks → Generate Answer (Gemini)
```

See [RAG_ARCHITECTURE.md](RAG_ARCHITECTURE.md) for detailed architecture documentation.

## 🔧 Configuration

### Chunking Parameters

Edit `chunk_and_embed.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # Characters per chunk
    chunk_overlap=100,    # Overlap between chunks
)
```

### Retrieval Parameters

Edit `rag_qa.py`:
```python
retrieved = retrieve(query, k=5)  # Number of chunks to retrieve
```

### LLM Model

Edit `rag_qa.py`:
```python
model = genai.GenerativeModel("gemini-2.5-flash")  # Change model here
```

## 🧪 Test Suite

The test suite includes 20 diverse questions covering:
- General pest and disease management
- Specific pest identification and control
- Disease symptoms and prevention
- Treatment methods and dosages
- Agricultural best practices

### Test Metrics Analyzed:
- Success rate
- Citation presence
- Answer length
- Error tracking

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

**Note**: The API key in the repository has been removed for security. You must provide your own.

## 🛡️ Security

- Never commit `.env` file with actual API keys
- `.env` is listed in `.gitignore`
- Use `.env.example` as a template for new setups

## 📚 Dependencies

- `langchain-community` - Document loaders
- `langchain-text-splitters` - Text chunking
- `sentence-transformers` - Embedding model
- `faiss-cpu` - Vector similarity search
- `google-generativeai` - LLM for answer generation
- `python-dotenv` - Environment variable management
- `pypdf` - PDF processing

## 🔍 How It Works

### Retrieval-Augmented Generation (RAG)

1. **Indexing Phase** (One-time):
   - Load PDF document
   - Split into overlapping chunks
   - Generate embeddings for each chunk
   - Store in FAISS vector database

2. **Query Phase** (Per question):
   - Convert user query to embedding
   - Search FAISS for most similar chunks
   - Retrieve top-K relevant text segments
   - Pass context + query to LLM
   - Generate answer with citations

### Why RAG?

- **Grounded Answers**: Responses based on actual document content
- **Citations**: Every fact traceable to source page
- **No Hallucinations**: LLM constrained to provided context
- **Efficient**: Only processes relevant sections
- **Scalable**: Can handle large documents and multiple files

## 📈 Performance

- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Chunk Size**: 500 characters with 100 overlap
- **Retrieval**: Top-5 most relevant chunks
- **Search**: Sub-second FAISS similarity search
- **Generation**: 2-5 seconds per answer (Gemini API)

## 🐛 Troubleshooting

### CUDA Errors

If you encounter CUDA errors, the code automatically uses CPU:
```python
embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
```

### API Key Errors

- Ensure your API key is valid and not expired
- Check that `.env` file exists and has the correct format
- Verify the key in [Google AI Studio](https://makersuite.google.com/app/apikey)

### Missing Files

If `faiss_index.bin` or `chunks.pkl` are missing:
```bash
python chunk_and_embed.py
```

## 📝 Example Questions

1. What are the main pests affecting cotton crops?
2. How to control whitefly in cotton crops?
3. What causes cotton leaf curl disease?
4. What are the recommended chemical pesticides for cotton pest control?
5. What preventive measures can reduce pest infestation in cotton?

See `test_rag.py` for 20 comprehensive test questions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available for educational and research purposes.

## 👥 Authors

Created for cotton pest and disease management research and advisory services.

## 🙏 Acknowledgments

- ICAR-CICR for the cotton advisory document
- Google AI for Gemini API
- LangChain community for document processing tools
- Sentence Transformers for embedding models
- FAISS for efficient similarity search

## 📞 Support

For issues or questions:
1. Check [RAG_ARCHITECTURE.md](RAG_ARCHITECTURE.md) for detailed documentation
2. Review the test results in `test_results_*.json`
3. Open an issue on GitHub

---

**Note**: Remember to update your `.env` file with a valid Google Gemini API key before running the system!
