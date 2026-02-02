# Cotton Advisory Chat - React + FastAPI

Professional full-stack web application for cotton pest and disease management advice.

## 🏗️ Architecture

```
frontend/          # Next.js React Application
├── app/           # App router pages
├── components/    # React components
└── public/        # Static assets

backend/           # FastAPI Python Backend
├── main.py        # API endpoints
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Google Gemini API key

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy embeddings (if not already present)
cp ../faiss_index.bin .
cp ../chunks.pkl .

# Set environment variable
export GEMINI_API_KEY=your_api_key_here  # On Windows: set GEMINI_API_KEY=your_key

# Run backend
python main.py
```

Backend will run on `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variable
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📦 Deployment to Vercel

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel
```

### Option 2: GitHub Integration

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Add environment variable: `GEMINI_API_KEY`
5. Deploy!

### Important: Set Environment Variables in Vercel

- `GEMINI_API_KEY`: Your Google Gemini API key
- `NEXT_PUBLIC_API_URL`: Your backend API URL

## 🎨 Features

- ✨ Modern, professional ChatGPT-like interface
- 🎯 Real-time chat with AI assistant
- 📱 Responsive design (mobile + desktop)
- 🔄 Conversation history
- 📋 Copy responses to clipboard
- 💾 Source citations for all answers
- ⚡ Fast responses with streaming
- 🛡️ Error handling and retry logic
- 🎨 Beautiful animations with Framer Motion

## 🧪 Testing

### Test Backend
```bash
curl http://localhost:8000/api/status
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"message":"What are cotton pests?"}'
```

### Test Frontend
Open `http://localhost:3000` and try asking questions!

## 📚 API Documentation

Once backend is running, visit:
- API Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## 🔧 Tech Stack

**Frontend:**
- Next.js 14
- React 18
- TailwindCSS
- Framer Motion
- TypeScript

**Backend:**
- FastAPI
- Python 3.8+
- FAISS
- Sentence Transformers
- Google Gemini AI

## 📁 Project Structure

```
Agentic-RAG-Cotton/
├── frontend/                 # React Next.js app
│   ├── app/
│   │   ├── page.tsx         # Main chat interface
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.js
├── backend/                  # FastAPI backend
│   ├── main.py              # API server
│   └── requirements.txt
├── vercel.json              # Vercel config
├── faiss_index.bin          # Vector database
├── chunks.pkl               # Text chunks
└── README_FULLSTACK.md      # This file
```

## 🐛 Troubleshooting

### Backend won't start
- Check if `chunks.pkl` and `faiss_index.bin` exist
- Verify `GEMINI_API_KEY` is set
- Check Python version (3.8+)

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

### Deployment issues
- Verify all environment variables in Vercel
- Check build logs for errors
- Ensure file sizes are within Vercel limits

## 📞 Support

For issues, please check:
1. Backend logs: `python main.py`
2. Frontend console: Browser DevTools
3. API docs: `http://localhost:8000/docs`

## 🚧 Future Enhancements

- [ ] User authentication
- [ ] Conversation persistence
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Image upload for pest identification
- [ ] Export chat history

---

**Built with ❤️ for Cotton Farmers**
