# RAG System Architecture - Cotton Advisory Document

## 🏗️ Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RAG SYSTEM PIPELINE                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   STAGE 1:      │      │   STAGE 2:       │      │   STAGE 3:      │
│   LOAD PDF      │ ───► │   CHUNK & EMBED  │ ───► │   RAG QA        │
│                 │      │                  │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

---

## 📊 Detailed Pipeline Workflow

### **STAGE 1: Document Loading** (`load_pdf.py`)

```
┌────────────────────────────────────────────────┐
│  INPUT: PDF Document                           │
│  File: ICAR-CICR_Advisory Pest and Disease    │
│        Management 2024.pdf                     │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ PyPDFLoader   │
         └───────┬───────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  OUTPUT: List of Document Objects             │
│  - Each page = 1 document                     │
│  - Contains: page_content + metadata          │
└────────────────────────────────────────────────┘
```

**Components:**
- **Library**: LangChain Community Document Loaders
- **Loader**: PyPDFLoader
- **Output**: List of document objects (one per page)

---

### **STAGE 2: Chunking & Embedding** (`chunk_and_embed.py`)

```
┌────────────────────────────────────────────────┐
│  INPUT: Document Pages                         │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │ Text Splitter    │
         │ chunk_size=500   │
         │ chunk_overlap=100│
         └────────┬─────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  Chunks Created                                │
│  (smaller text segments with metadata)         │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │ Embedding Model  │
         │ all-MiniLM-L6-v2 │
         └────────┬─────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  Vector Embeddings (384-dim vectors)           │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │  FAISS Index     │
         │  (IndexFlatL2)   │
         └────────┬─────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  OUTPUTS:                                      │
│  1. faiss_index.bin  (vector database)         │
│  2. chunks.pkl       (text + metadata)         │
└────────────────────────────────────────────────┘
```

**Components:**
- **Text Splitter**: RecursiveCharacterTextSplitter
  - Chunk size: 500 characters
  - Chunk overlap: 100 characters
- **Embedding Model**: SentenceTransformer ('all-MiniLM-L6-v2')
- **Vector Database**: FAISS (Facebook AI Similarity Search)
  - IndexFlatL2 (L2 distance metric)
- **Storage**: 
  - `faiss_index.bin` - vector index
  - `chunks.pkl` - text chunks and metadata

---

### **STAGE 3: RAG Question Answering** (`rag_qa.py`)

```
┌────────────────────────────────────────────────┐
│  INPUT: User Query (Natural Language)          │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │ Load Resources   │
         │ - FAISS Index    │
         │ - Chunks.pkl     │
         │ - Embedder       │
         └────────┬─────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  RETRIEVAL PHASE                               │
│  ┌──────────────────────────────────────────┐ │
│  │ 1. Query → Embedding (384-dim vector)    │ │
│  │ 2. FAISS Similarity Search (k=5)         │ │
│  │ 3. Retrieve Top-5 Most Relevant Chunks   │ │
│  └──────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  CONTEXT FORMATTING                            │
│  For each chunk:                               │
│  [Source p.X] {chunk_text}                     │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  GENERATION PHASE                              │
│  ┌──────────────────────────────────────────┐ │
│  │ 1. Build Prompt:                         │ │
│  │    - System instruction                  │ │
│  │    - Retrieved context                   │ │
│  │    - User query                          │ │
│  │ 2. Send to LLM (Gemini 2.5 Flash)       │ │
│  │ 3. Generate Answer with Citations       │ │
│  └──────────────────────────────────────────┘ │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  OUTPUT: Answer with Source Citations         │
│  Example: "Based on the document [Source p.5],│
│            cotton pests can be managed by..."  │
└────────────────────────────────────────────────┘
```

**Components:**
- **Retriever**: 
  - Uses same embedding model (all-MiniLM-L6-v2)
  - FAISS similarity search (Top-K=5)
- **LLM**: Google Gemini 2.5 Flash
- **Citation System**: Automatically includes page numbers from metadata

---

## 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **PDF Loading** | PyPDFLoader (LangChain) | Extract text from PDF documents |
| **Text Splitting** | RecursiveCharacterTextSplitter | Break documents into manageable chunks |
| **Embeddings** | SentenceTransformer (all-MiniLM-L6-v2) | Convert text to 384-dim vectors |
| **Vector DB** | FAISS (IndexFlatL2) | Fast similarity search |
| **LLM** | Google Gemini 2.5 Flash | Generate contextual answers |
| **Storage** | Pickle + Binary | Persist chunks and index |

---

## 📂 Data Flow

```
PDF Document
    ↓
Pages (Document Objects)
    ↓
Chunks (500 chars, 100 overlap)
    ↓
Embeddings (384-dim vectors)
    ↓
FAISS Index + Metadata Storage
    ↓
Query → Retrieve → Generate → Answer
```

---

## 🔑 Key Features

### 1. **Chunking Strategy**
- **Chunk Size**: 500 characters
- **Overlap**: 100 characters
- **Purpose**: Maintain context across chunk boundaries

### 2. **Embedding Model**
- **Model**: all-MiniLM-L6-v2
- **Dimensions**: 384
- **Type**: Lightweight, fast, good accuracy

### 3. **Retrieval**
- **Method**: Semantic similarity search
- **Metric**: L2 distance (Euclidean)
- **Top-K**: 5 most relevant chunks

### 4. **Citation System**
- Automatically includes source page numbers
- Format: `[Source p.X]`
- Traceable back to original document

### 5. **LLM Configuration**
- **Model**: Gemini 2.5 Flash
- **Constraint**: Answer ONLY from provided context
- **Output**: Citations for every fact

---

## 🚀 Execution Workflow

### **Setup Phase (One-time)**
1. Run `load_pdf.py` - Verify PDF loading
2. Run `chunk_and_embed.py` - Create FAISS index
   - Generates: `faiss_index.bin`, `chunks.pkl`

### **Query Phase (Repeated)**
3. Run `rag_qa.py` - Interactive Q&A
   - Input: User question
   - Output: Contextualized answer with citations

---

## 📈 System Metrics

- **Document**: ICAR-CICR Cotton Advisory (Pest & Disease Management 2024)
- **Chunks**: ~N chunks (depends on document size)
- **Vector Dimensions**: 384
- **Retrieval Speed**: Fast (FAISS optimized)
- **Context Window**: Top-5 chunks per query

---

## 💡 RAG Advantages

1. **Grounded Answers**: Responses based on actual document content
2. **Citations**: Every fact traceable to source page
3. **Efficient**: Only retrieves relevant chunks
4. **Scalable**: Can handle multiple documents
5. **Transparent**: Shows sources for verification

---

## 🔄 Future Enhancements

- [ ] Multi-document support
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking retrieved chunks
- [ ] Query expansion/refinement
- [ ] Conversation history
- [ ] Advanced chunking strategies
- [ ] Response evaluation metrics

---

## 📝 File Structure

```
Agentic-RAG/
├── load_pdf.py           # Stage 1: PDF loading
├── chunk_and_embed.py    # Stage 2: Chunking + embedding
├── rag_qa.py             # Stage 3: RAG Q&A
├── document/             # Source PDF files
├── faiss_index.bin       # Generated vector index
├── chunks.pkl            # Generated chunk storage
└── RAG_ARCHITECTURE.md   # This file
```

---

**Created**: February 2, 2026
**System**: Cotton Advisory Document RAG Pipeline
**Purpose**: Clear architecture documentation for RAG workflow
