# Vercel Deployment Guide

## Prerequisites
- GitHub repository: https://github.com/pavanpavaman/Agentic-RAG-Cotton
- Vercel account (free tier works)
- Google Gemini API key

## Step-by-Step Deployment

### 1. Sign Up/Login to Vercel
- Go to [vercel.com](https://vercel.com)
- Sign up or login with your GitHub account
- This will connect your GitHub repositories to Vercel

### 2. Import Your Project
- Click **"Add New..."** → **"Project"**
- Select **"Import Git Repository"**
- Find and select: **pavanpavaman/Agentic-RAG-Cotton**
- Click **"Import"**

### 3. Configure Project Settings

#### Framework Preset
- **Framework Preset**: Next.js (auto-detected)

#### Root Directory
- Click **"Edit"** next to Root Directory
- Select: **`frontend`**
- This is CRITICAL as your Next.js app is in the frontend folder

#### Build & Output Settings (Auto-filled)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 4. Configure Environment Variables

Click **"Environment Variables"** and add the following:

#### For Production Environment:

**GEMINI_API_KEY**
```
your_actual_gemini_api_key_here
```
Get your key from: https://aistudio.google.com/app/apikey

**NEXT_PUBLIC_API_URL**
```
https://your-app-name.vercel.app/api
```
Note: Replace `your-app-name` with your actual Vercel app name (shown at the top)
You can also update this after the first deployment.

**ALLOWED_ORIGINS** (for backend CORS)
```
https://your-app-name.vercel.app
```
Again, replace with your actual domain.

> **Important**: Mark all variables for **Production** environment
> You can add them for Preview and Development environments too if needed

### 5. Deploy
- Click **"Deploy"**
- Wait 2-5 minutes for the build to complete
- Vercel will show you the deployment progress

### 6. Post-Deployment Configuration

After first deployment:

1. **Note Your Deployment URL**
   - It will be something like: `https://agentic-rag-cotton-abc123.vercel.app`

2. **Update Environment Variables**
   - Go to your project dashboard
   - Click **"Settings"** → **"Environment Variables"**
   - Update `NEXT_PUBLIC_API_URL` with your actual domain:
     ```
     https://your-actual-domain.vercel.app/api
     ```
   - Update `ALLOWED_ORIGINS` with your actual domain

3. **Redeploy**
   - Go to **"Deployments"**
   - Click the three dots (...) on the latest deployment
   - Select **"Redeploy"**

### 7. Verify Deployment

Visit your app URL and test:
- ✅ Frontend loads correctly
- ✅ You can type messages
- ✅ AI responds with cotton advisory information
- ✅ Chat history works
- ✅ No CORS errors in browser console

## Important Notes

### Backend API on Vercel
Your FastAPI backend needs to be deployed separately or included in the monorepo deployment. Vercel supports Python serverless functions, but FAISS and large dependencies may have limitations.

**Alternative Approach:**
1. Deploy frontend to Vercel (as done above)
2. Deploy backend to:
   - **Railway.app** (Recommended for Python/FastAPI)
   - **Render.com**
   - **Heroku**
   - **AWS Lambda** (with container)

3. Update `NEXT_PUBLIC_API_URL` to point to your backend deployment

### Backend Deployment (Railway.app Example)

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Select the `backend` folder
4. Add environment variables:
   - `GEMINI_API_KEY`
   - `ALLOWED_ORIGINS` (your Vercel frontend URL)
5. Deploy
6. Copy the Railway URL and update `NEXT_PUBLIC_API_URL` in Vercel

### Files and Database
- Make sure `faiss_index.bin` and `chunks.pkl` are in your repository
- The PDF document should be in the `document/` folder
- These files should NOT be in `.gitignore`

### Environment Variables Reference

| Variable | Where | Example |
|----------|-------|---------|
| `GEMINI_API_KEY` | Backend | `AIza...` |
| `NEXT_PUBLIC_API_URL` | Frontend (Vercel) | `https://api.example.com` |
| `ALLOWED_ORIGINS` | Backend | `https://frontend.vercel.app` |
| `DOCUMENT_PATH` | Backend (optional) | `./document/file.pdf` |

## Troubleshooting

### Build Fails
- Check that Root Directory is set to `frontend`
- Verify `package.json` exists in frontend folder
- Check build logs for specific errors

### API Calls Fail
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings on backend
- Ensure backend is running and accessible
- Check browser console for specific errors

### 404 Errors
- Verify `vercel.json` is in the root directory
- Check routing configuration
- Ensure frontend builds successfully

### Environment Variables Not Working
- Ensure variables start with `NEXT_PUBLIC_` for client-side access
- Redeploy after changing environment variables
- Check variable names match exactly (case-sensitive)

## Custom Domain (Optional)

1. Go to project **Settings** → **Domains**
2. Add your custom domain
3. Follow Vercel's DNS configuration instructions
4. Update `NEXT_PUBLIC_API_URL` and `ALLOWED_ORIGINS` with new domain

## Monitoring

- **Analytics**: Vercel provides built-in analytics
- **Logs**: View real-time logs in Vercel dashboard
- **Performance**: Check Web Vitals in the dashboard

## Costs

- **Free Tier Includes**:
  - 100 GB bandwidth/month
  - Unlimited deployments
  - Automatic HTTPS
  - Preview deployments for PRs

- **Upgrade Needed For**:
  - High traffic (>100 GB/month)
  - Team collaboration
  - Advanced analytics

## Support

- Vercel Documentation: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions

---

**Repository**: https://github.com/pavanpavaman/Agentic-RAG-Cotton
**Status**: ✅ Ready for Production Deployment
