# Cotton Advisory RAG Chat System

AI-Powered Cotton Pest & Disease Management Chat Assistant built with Next.js, FastAPI, and RAG technology.

## Features

- Modern ChatGPT-like interface
- Real-time AI responses powered by Google Gemini
- Citation-backed answers from ICAR-CICR Advisory 2024
- Conversation history management
- Responsive design for all devices

## Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Markdown** - Message rendering

### Backend
- **FastAPI** - Python web framework
- **FAISS** - Vector database for semantic search
- **Sentence Transformers** - Text embeddings
- **Google Gemini** - LLM for response generation
- **LangChain** - Document processing

## Local Development

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Google Gemini API key

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Agentic-RAG
```

2. **Backend Setup**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Generate embeddings (first time only)
python chunk_and_embed.py

# Start backend server
cd backend
uvicorn main:app --reload
```

3. **Frontend Setup**
```bash
# Install dependencies
cd frontend
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Deployment to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier works)
- Google Gemini API key

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Configure project:
     - Framework Preset: **Next.js**
     - Root Directory: **frontend**
     - Build Command: **npm run build**
     - Output Directory: **.next**
   
3. **Set Environment Variables** in Vercel:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `NEXT_PUBLIC_API_URL`: Your Vercel app URL + `/api`
   - `ALLOWED_ORIGINS`: Your Vercel frontend URL

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Access your live app!

### Important Notes
- The `/document` folder and generated files (`faiss_index.bin`, `chunks.pkl`) should be included in deployment
- Environment variables must be set in Vercel dashboard
- CORS is configured to allow requests from your frontend domain

## Project Structure

```
Agentic-RAG/
├── frontend/              # Next.js frontend application
│   ├── app/              # Next.js app directory
│   │   ├── page.tsx     # Main chat interface
│   │   ├── layout.tsx   # Root layout
│   │   └── globals.css  # Global styles
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
│
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints and RAG logic
│   └── requirements.txt # Backend dependencies
│
├── document/            # PDF documents for RAG
│   └── ICAR-CICR_Advisory Pest and Disease Management 2024.pdf
│
├── faiss_index.bin     # Generated vector index
├── chunks.pkl          # Generated chunk storage
├── chunk_and_embed.py  # Document processing script
├── rag_qa.py          # RAG query logic
└── vercel.json        # Vercel deployment config
```

## API Endpoints

### `GET /`
Health check endpoint

### `POST /api/chat`
Main chat endpoint
- **Request Body**: `{ "message": "string", "context": [] }`
- **Response**: `{ "answer": "string", "sources": [] }`

### `GET /api/health`
System health status

## Environment Variables

### Backend (.env)
```env
GEMINI_API_KEY=your_api_key_here
DOCUMENT_PATH=./document/ICAR-CICR_Advisory Pest and Disease Management 2024.pdf
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open a GitHub issue.
