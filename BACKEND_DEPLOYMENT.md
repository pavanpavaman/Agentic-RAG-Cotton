# Backend Deployment to Railway - Simple Steps

## What We're Deploying
The FastAPI backend (Python API that handles AI responses)

## Why Railway?
- ✅ Free tier available
- ✅ Supports Python with large dependencies (FAISS, transformers)
- ✅ Easy to deploy from GitHub
- ✅ Provides public URL automatically

---

## Step-by-Step Backend Deployment

### Step 1: Sign Up for Railway
1. Go to https://railway.app
2. Click **"Login"**
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your repositories

### Step 2: Create New Project
1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Find and click **"pavanpavaman/Agentic-RAG-Cotton"**

### Step 3: Configure Deployment ⚠️ IMPORTANT

After selecting your repository, you'll see the project page. **STOP THE BUILD FIRST!**

#### Cancel the Initial Build
1. Railway starts building automatically
2. Click the **X** or **"Cancel"** button on the build that's running
3. We need to configure settings first!

#### Set Root Directory (CRITICAL)
1. Click the **"Settings"** tab (top right)
2. Scroll down to **"Source"** section
3. Find **"Root Directory"** 
4. Click **"Edit"** or the field
5. Type: `backend`
6. Press **Enter** or click **"Update"**

#### Set Start Command
1. Still in **Settings** tab
2. Scroll to **"Deploy"** section
3. Find **"Custom Start Command"**
4. Click the field and enter:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Press **Enter** or click **"Update"**

#### Set Python Version (Optional but Recommended)
1. In **Settings** → **"Environment"** section
2. Find **"Builder"** or **"Nixpacks Plan"**
3. Click **"Add Variable"** if you see it
4. Or scroll to **"Nixpacks Config File"**
5. We'll use Railway's auto-detect for now

### Step 4: Add Environment Variables

**CRITICAL:** Add these in the **"Variables"** tab:

#### 1. GEMINI_API_KEY
```
Click "+ New Variable"
Name: GEMINI_API_KEY
Value: [Your actual Google Gemini API key]
```
Get your API key from: https://aistudio.google.com/app/apikey

#### 2. PORT
```
Name: PORT
Value: 8000
```

#### 3. ALLOWED_ORIGINS
```
Name: ALLOWED_ORIGINS
Value: https://your-frontend-url.vercel.app
```
Replace with your actual Vercel frontend URL from earlier!

#### 4. DOCUMENT_PATH (optional)
```
Name: DOCUMENT_PATH
Value: ../document/ICAR-CICR_Advisory Pest and Disease Management 2024.pdf
```

Click **"Add"** for each variable.

### Step 5: Deploy!
1. Go to **"Deployments"** tab
2. Click **"Deploy"** button (top right) or **"Redeploy"**
3. Wait 3-5 minutes for build to complete
4. Watch the logs - you should see:
   - ✅ Installing from `backend/requirements.txt`
   - ✅ `uvicorn` starting
   - ✅ "Application startup complete"

### Step 6: Get Your Backend URL
1. Go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Railway will create a URL like: `https://your-app.up.railway.app`
5. **COPY THIS URL** - you'll need it!

### Step 7: Test Your Backend
Visit: `https://your-app.up.railway.app/docs`

You should see the FastAPI Swagger documentation!

---

## Connect Frontend to Backend

Now that backend is deployed, update your frontend:

### Step 1: Go Back to Vercel
1. Go to https://vercel.com
2. Open your frontend project
3. Click **"Settings"** tab
4. Click **"Environment Variables"**

### Step 2: Update API URL
1. Find **"NEXT_PUBLIC_API_URL"**
2. Click **"Edit"** (three dots)
3. Change value to:
   ```
   https://your-app.up.railway.app
   ```
   (Use YOUR actual Railway URL - NO /api at the end!)
4. Click **"Save"**

### Step 3: Redeploy Frontend
1. Go to **"Deployments"** tab
2. Click the **three dots (...)** on latest deployment
3. Click **"Redeploy"**
4. Wait 1-2 minutes

---

## Test Everything!

### 1. Visit Your Frontend
Go to your Vercel URL: `https://your-app.vercel.app`

### 2. Try Sending a Message
Type: "What are the main pests affecting cotton?"

### 3. Expected Result
✅ You should get an AI response with cotton pest information!

---

## Troubleshooting

### Backend "Application Error"
**Check:**
1. Did you add `GEMINI_API_KEY`?
2. Are `faiss_index.bin` and `chunks.pkl` in your repo?
3. Check Railway logs for errors

**Fix:** 
- Go to Railway project
- Click **"Deployments"** → View logs
- Look for specific error messages

### Build Failed - "Installing Wrong Requirements"
**Problem:** Railway installing from root `requirements.txt` instead of `backend/requirements.txt`

**Fix:**
1. Go to **Settings** tab
2. Check **"Root Directory"** is set to `backend`
3. If not, update it to `backend`
4. Go to **"Deployments"** tab
5. Click **"Redeploy"** button
6. Watch logs - should now use `backend/requirements.txt`

**Still failing?** Try the **Render.com alternative** below!

### Frontend "Failed to fetch"
**Check:**
1. Is backend URL correct in Vercel env variables?
2. Did you redeploy frontend after changing env variables?
3. Check browser console for CORS errors

**Fix:**
- Update `ALLOWED_ORIGINS` in Railway to match your Vercel URL
- Redeploy both frontend and backend

### "CORS Error"
**Fix:**
1. In Railway, update `ALLOWED_ORIGINS` variable:
   ```
   https://your-frontend.vercel.app,https://your-frontend.vercel.app/
   ```
   (Add both with and without trailing slash)
2. Redeploy backend

### Backend Takes Long to Respond (Cold Start)
- Normal for free tier
- First request after inactivity takes 30-60 seconds
- Subsequent requests are fast
- **Solution:** Upgrade to paid tier or keep backend warm

---

## Alternative: Deploy to Render.com (If Railway Fails)

Render.com is more straightforward for Python apps with specific folder structures.

### Step 1: Sign Up for Render
1. Go to https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Choose **"Sign in with GitHub"**
4. Authorize Render

### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Find and click **"Connect"** next to `pavanpavaman/Agentic-RAG-Cotton`

### Step 3: Configure Service

Fill in these fields:

**Name:** `cotton-advisory-backend` (or any name you like)

**Region:** Choose closest to you

**Branch:** `main`

**Root Directory:** `backend` ⚠️ IMPORTANT

**Runtime:** `Python 3`

**Build Command:** 
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:** `Free` (select from dropdown)

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** for each:

1. **Key:** `GEMINI_API_KEY`, **Value:** `your_actual_api_key`
2. **Key:** `PORT`, **Value:** `10000`
3. **Key:** `ALLOWED_ORIGINS`, **Value:** `https://your-frontend.vercel.app`
4. **Key:** `PYTHON_VERSION`, **Value:** `3.11.0`

### Step 5: Create Web Service
1. Click **"Create Web Service"** button at bottom
2. Wait 3-5 minutes for deployment
3. Watch the logs in real-time

### Step 6: Get Your URL
Once deployed, you'll see:
- ✅ Green "Live" indicator
- 🔗 URL at top: `https://cotton-advisory-backend.onrender.com`
- Copy this URL!

### Step 7: Connect to Frontend
Same as Railway - update `NEXT_PUBLIC_API_URL` in Vercel to your Render URL.

---

## Alternative Backend Hosts

If Railway doesn't work, try these:

### Render.com
- Similar to Railway
- Free tier available
- Good Python support
- https://render.com

### Heroku
- Classic platform
- Free tier removed, paid only
- Very reliable
- https://heroku.com

### Fly.io
- Free tier available
- Good for Docker
- Fast deployments
- https://fly.io

---

## Files That Must Be in Repository

Make sure these exist (they should already):
- ✅ `backend/main.py`
- ✅ `backend/requirements.txt`
- ✅ `faiss_index.bin` (in root)
- ✅ `chunks.pkl` (in root)
- ✅ `document/ICAR-CICR_Advisory Pest and Disease Management 2024.pdf`

---

## Quick Local Testing

Test backend locally before deploying:

```bash
# Activate virtual environment
cd E:\Agentic-RAG
.venv310\Scripts\activate

# Set environment variable
$env:GEMINI_API_KEY="your_api_key"

# Run backend
cd backend
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

---

## Cost Summary

### Free Tier Limits
- **Railway**: $5 free credit/month (~500 hours)
- **Vercel**: Unlimited deployments, 100GB bandwidth

### If You Need More
- Railway Pro: $5/month (includes $5 usage credit)
- Vercel Pro: $20/month (more bandwidth)

---

## Environment Variables Summary

### Railway (Backend)
| Variable | Value | Required |
|----------|-------|----------|
| GEMINI_API_KEY | Your API key | ✅ Yes |
| PORT | 8000 | ✅ Yes |
| ALLOWED_ORIGINS | Your Vercel URL | ✅ Yes |
| DOCUMENT_PATH | ../document/file.pdf | Optional |

### Vercel (Frontend)
| Variable | Value | Required |
|----------|-------|----------|
| NEXT_PUBLIC_API_URL | Railway backend URL | ✅ Yes |

---

**Your app should now be fully deployed and working! 🎉**

- Frontend: https://your-app.vercel.app
- Backend: https://your-app.up.railway.app
- Docs: https://your-app.up.railway.app/docs
