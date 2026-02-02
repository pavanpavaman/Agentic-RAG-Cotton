# Cotton Advisory RAG System

A Retrieval-Augmented Generation (RAG) system for answering questions about cotton pest and disease management based on the ICAR-CICR Advisory document.

## 🚀 Features

- **PDF Document Processing**: Load and extract text from agricultural advisory PDFs
- **Semantic Search**: FAISS-based vector similarity search for relevant content retrieval
- **Context-Aware Answers**: Google Gemini AI generates answers with source citations
- **Comprehensive Testing**: Test suite with 20 cotton-specific questions
- **Secure Configuration**: Environment variable management for API keys

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- PDF document about cotton pest and disease management

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/Agentic-RAG.git
cd Agentic-RAG
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## 📁 Project Structure

```
Agentic-RAG/
├── load_pdf.py              # Stage 1: PDF loading
├── chunk_and_embed.py       # Stage 2: Chunking + embedding
├── rag_qa.py                # Stage 3: RAG Q&A system
├── test_rag.py              # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
├── RAG_ARCHITECTURE.md      # Detailed system architecture
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
