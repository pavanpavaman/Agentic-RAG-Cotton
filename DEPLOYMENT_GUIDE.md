# Deployment Guide - Cotton RAG System

## ⚠️ IMPORTANT: API Key Required

The previous Gemini API key has **EXPIRED**. You need to get a new one before testing or deploying.

### Get a New API Key:
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key
5. Update `.env` file:
   ```
   GEMINI_API_KEY=your_new_api_key_here
   ```

---

## ✅ Pre-Deployment Checklist

### Security ✓
- [x] API key moved to `.env` file
- [x] `.env` added to `.gitignore`
- [x] `.env.example` created as template
- [x] Sensitive data removed from code

### Code Quality ✓
- [x] Environment variable loading implemented
- [x] CPU-only mode configured for embedding (fixes CUDA errors)
- [x] Error handling in place
- [x] Dependencies documented in `requirements.txt`

### Documentation ✓
- [x] `README.md` with setup instructions
- [x] `RAG_ARCHITECTURE.md` with detailed pipeline
- [x] `.env.example` with configuration template
- [x] Code comments and docstrings

### Testing ⚠️
- [x] Test suite created with 20 questions
- [ ] **ACTION REQUIRED**: Get new API key and run tests
- [ ] Validate answer quality and citations

---

## 🚀 Deployment Steps

### 1. Update API Key (REQUIRED)

```bash
# Edit .env file
GEMINI_API_KEY=your_new_api_key_here
```

### 2. Run Tests

```bash
# Make sure you're in the project directory
cd E:\Agentic-RAG

# Run comprehensive tests
python test_rag.py
```

**Expected Results:**
- 20/20 questions answered successfully
- All answers should have [Source p.X] citations
- Average answer length: 50-150 words
- No errors

### 3. Review Test Results

Check the generated `test_results_YYYYMMDD_HHMMSS.json` file:
- Verify answer quality
- Check citation presence
- Review any errors

### 4. Initialize Git Repository

```bash
cd E:\Agentic-RAG
git init
git add .
git commit -m "Initial commit: Cotton RAG system with security and testing"
```

### 5. Create GitHub Repository

**Option A: Using GitHub CLI**
```bash
gh repo create Agentic-RAG --public --source=. --remote=origin
git push -u origin main
```

**Option B: Using GitHub Web Interface**
1. Go to https://github.com/new
2. Repository name: `Agentic-RAG`
3. Description: "RAG system for cotton pest and disease management"
4. Choose Public or Private
5. DO NOT initialize with README (you already have one)
6. Click "Create repository"
7. Follow the commands shown:
   ```bash
   git remote add origin https://github.com/yourusername/Agentic-RAG.git
   git branch -M main
   git push -u origin main
   ```

### 6. Verify GitHub Upload

Check that these files are present:
- ✓ `README.md`
- ✓ `RAG_ARCHITECTURE.md`
- ✓ `load_pdf.py`
- ✓ `chunk_and_embed.py`
- ✓ `rag_qa.py`
- ✓ `test_rag.py`
- ✓ `requirements.txt`
- ✓ `.gitignore`
- ✓ `.env.example`

Check that these files are **NOT** uploaded:
- ✗ `.env` (should be ignored)
- ✗ `faiss_index.bin` (should be ignored)
- ✗ `chunks.pkl` (should be ignored)
- ✗ `test_results_*.json` (should be ignored)

---

## 🧪 Testing Workflow

### Before Deploying:

1. **Get Valid API Key**
   - Current key is expired
   - Get new key from Google AI Studio

2. **Run Full Test Suite**
   ```bash
   python test_rag.py
   ```

3. **Analyze Results**
   - Success rate should be 95-100%
   - All answers should have citations
   - No API errors

4. **Manual Spot Checks**
   ```bash
   python rag_qa.py
   ```
   Test with questions like:
   - "What are the main cotton pests?"
   - "How to control bollworm?"
   - "What causes leaf curl disease?"

5. **Verify Answers Against Document**
   - Check that citations are accurate
   - Verify facts match source document
   - Ensure no hallucinations

### Quality Metrics:

**Excellent:**
- ✓ 100% success rate
- ✓ 100% answers with citations
- ✓ Average 75-150 words per answer
- ✓ Factually accurate

**Good:**
- ✓ 90-99% success rate
- ✓ 90-99% answers with citations
- ✓ No critical errors

**Needs Improvement:**
- ⚠️ <90% success rate
- ⚠️ <90% citations
- ⚠️ Factual inaccuracies

---

## 🔧 Post-Deployment Setup (For Users)

Once on GitHub, users should:

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/Agentic-RAG.git
   cd Agentic-RAG
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add their API key
   ```

4. **Generate Embeddings**
   ```bash
   python chunk_and_embed.py
   ```

5. **Start Using**
   ```bash
   python rag_qa.py
   ```

---

## 📋 Known Issues & Solutions

### Issue 1: API Key Expired ⚠️
**Error**: `400 API key expired. Please renew the API key.`

**Solution**: 
- Get new API key from https://makersuite.google.com/app/apikey
- Update `.env` file with new key

### Issue 2: CUDA Error ✅ FIXED
**Error**: `CUDA error: no kernel image is available`

**Solution**: 
- Fixed by forcing CPU mode in `rag_qa.py`
- `embedder = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')`

### Issue 3: Deprecation Warning ⚠️
**Warning**: `google.generativeai` package deprecated

**Solution** (Optional):
- Consider migrating to `google.genai` package in future
- Current code still works despite warning

### Issue 4: Missing Files
**Error**: `FileNotFoundError: faiss_index.bin`

**Solution**:
- Run `python chunk_and_embed.py` first
- This generates required files

---

## 🎯 Next Steps After Deployment

### Immediate:
1. ✅ Get new Google Gemini API key
2. ✅ Run test suite with valid key
3. ✅ Review and validate test results
4. ✅ Push to GitHub

### Short-term Improvements:
- [ ] Add more diverse test questions
- [ ] Implement response quality scoring
- [ ] Add support for multiple documents
- [ ] Create web interface (Streamlit/Gradio)

### Long-term Enhancements:
- [ ] Migrate to `google.genai` package
- [ ] Add hybrid search (keyword + semantic)
- [ ] Implement conversation memory
- [ ] Add re-ranking for better retrieval
- [ ] Create API endpoint for integration

---

## 📊 Testing Summary Template

After running tests with valid API key, document results:

```
## Test Results

**Date**: [YYYY-MM-DD]
**Total Questions**: 20
**Success Rate**: [X%]
**Citations Present**: [X%]
**Average Word Count**: [X words]

**Quality Assessment**: [Excellent/Good/Needs Improvement]

**Sample Answers**:
1. Q: "What are the main pests affecting cotton crops?"
   A: [Copy answer here]
   
2. Q: "How to control whitefly in cotton crops?"
   A: [Copy answer here]

**Issues Found**: [None / List issues]

**Recommendations**: [Any improvements needed]
```

---

## 🔒 Security Reminders

- ✓ Never commit `.env` file
- ✓ Never hardcode API keys in source code
- ✓ Use `.env.example` for documentation
- ✓ Rotate API keys periodically
- ✓ Review `.gitignore` before each commit
- ✓ Check GitHub repo to ensure no secrets uploaded

---

## 📞 Support

If you encounter issues:

1. Check this deployment guide
2. Review `README.md`
3. Consult `RAG_ARCHITECTURE.md`
4. Check error messages in test results
5. Verify API key validity

---

**STATUS**: Ready for deployment after API key update ✅

**PRIORITY ACTION**: Get new Gemini API key and run tests! 🔑
