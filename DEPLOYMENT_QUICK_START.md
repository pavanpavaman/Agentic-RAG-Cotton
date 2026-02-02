# 🚀 Quick Deployment Guide

## Complete Deployment in 2 Steps

### Step 1: Deploy Frontend (5 minutes)
📄 **Follow:** [FRONTEND_DEPLOYMENT.md](FRONTEND_DEPLOYMENT.md)

**Quick Summary:**
1. Login to https://vercel.com with GitHub
2. Import your repo: `pavanpavaman/Agentic-RAG-Cotton`
3. **Set Root Directory to: `frontend`** ⚠️ IMPORTANT
4. Add env variable: `NEXT_PUBLIC_API_URL=http://localhost:8000`
5. Click Deploy
6. **Save your Vercel URL** (e.g., `https://your-app.vercel.app`)

---

### Step 2: Deploy Backend (5 minutes)
📄 **Follow:** [BACKEND_DEPLOYMENT.md](BACKEND_DEPLOYMENT.md)

**Quick Summary:**
1. Login to https://railway.app with GitHub
2. Deploy from repo: `pavanpavaman/Agentic-RAG-Cotton`
3. Set root directory: `backend`
4. Add environment variables:
   - `GEMINI_API_KEY` = your API key
   - `PORT` = 8000
   - `ALLOWED_ORIGINS` = your Vercel URL from Step 1
5. Generate domain
6. **Copy your Railway URL** (e.g., `https://your-app.up.railway.app`)

---

### Step 3: Connect Them (2 minutes)
1. Go back to **Vercel** → Your Project → **Settings** → **Environment Variables**
2. Edit `NEXT_PUBLIC_API_URL` to your Railway URL
3. Go to **Deployments** → Click **...** → **Redeploy**
4. Done! 🎉

---

## Test Your Deployed App

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Type: "What are the main pests affecting cotton?"
3. Get AI response! ✅

---

## What You Get

- ✅ **Frontend**: Beautiful chat interface on Vercel
- ✅ **Backend**: AI-powered API on Railway
- ✅ **100% Free** (with free tier limits)
- ✅ **Auto HTTPS** on both platforms
- ✅ **Auto deployments** when you push to GitHub

---

## Detailed Guides

- **Frontend Only:** [FRONTEND_DEPLOYMENT.md](FRONTEND_DEPLOYMENT.md)
- **Backend Only:** [BACKEND_DEPLOYMENT.md](BACKEND_DEPLOYMENT.md)
- **Troubleshooting:** Check both guides above

---

## Repository
🔗 https://github.com/pavanpavaman/Agentic-RAG-Cotton

---

## Need Help?

**Common Issues:**

1. **"Build Failed"** → Check Root Directory is set to `frontend`
2. **"CORS Error"** → Check `ALLOWED_ORIGINS` in Railway matches Vercel URL
3. **"API not responding"** → Check Railway deployment logs
4. **"Slow first request"** → Normal cold start on free tier (30-60 sec)

**Still stuck?** Check detailed guides above or create a GitHub issue.
