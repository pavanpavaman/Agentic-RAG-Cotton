# Frontend Deployment to Vercel - Simple Steps

## What We're Deploying
Only the Next.js frontend (the chat interface)

## Prerequisites
- GitHub account (you already have this)
- Vercel account (free) - sign up at https://vercel.com with your GitHub account

---

## Step-by-Step Frontend Deployment

### Step 1: Login to Vercel
1. Go to https://vercel.com
2. Click **"Sign Up"** or **"Login"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub repositories

### Step 2: Create New Project
1. On Vercel dashboard, click **"Add New..."** button (top right)
2. Select **"Project"** from dropdown
3. You'll see "Import Git Repository" page

### Step 3: Import Your Repository
1. Find **"pavanpavaman/Agentic-RAG-Cotton"** in the list
2. Click **"Import"** button next to it
3. If you don't see it, click **"Adjust GitHub App Permissions"** to grant access

### Step 4: Configure the Project

You'll see a configuration screen. Here's what to set:

#### Project Name
- Leave as default or change to something like: `cotton-advisory-chat`

#### Framework Preset
- Should auto-detect as **"Next.js"**
- If not, select **"Next.js"** from dropdown

#### Root Directory
**This is CRITICAL:**
1. Click **"Edit"** next to "Root Directory"
2. Click on the **"frontend"** folder
3. Click **"Continue"**
4. You should now see: `Root Directory: frontend`

#### Build and Output Settings
- Keep defaults (should show):
  - Build Command: `npm run build`
  - Output Directory: `.next`
  - Install Command: `npm install`

### Step 5: Environment Variables

Click **"Environment Variables"** section to expand it.

Add this ONE variable for now:

**Variable Name:**
```
NEXT_PUBLIC_API_URL
```

**Value:**
```
http://localhost:8000
```
(We'll update this later when backend is deployed)

**Select:** Production, Preview, Development (check all three)

Click **"Add"**

### Step 6: Deploy!
1. Click the big **"Deploy"** button
2. Wait 2-3 minutes while Vercel builds your frontend
3. You'll see a progress screen with logs

### Step 7: Success!
Once deployed, you'll see:
- ✅ A congratulations screen
- 🔗 Your live URL (something like: `https://cotton-advisory-chat.vercel.app`)
- Click **"Visit"** to see your app

---

## What You'll See

Your frontend is now live, BUT:
- ❌ Clicking "Send" won't work yet (backend not connected)
- ✅ The UI will load perfectly
- ✅ You can type messages
- ✅ The interface looks great

**Next:** Deploy the backend (see BACKEND_DEPLOYMENT.md)

---

## Quick Commands to Test Locally

Want to test the frontend locally first?

```bash
cd E:\Agentic-RAG\frontend
npm install
npm run dev
```

Then visit: http://localhost:3000

---

## Troubleshooting

### "Build Failed"
- **Check:** Did you set Root Directory to `frontend`?
- **Check:** Build logs for specific error
- **Fix:** Go to Project Settings → General → Root Directory → Edit

### "Page Not Found"
- **Check:** Did deployment succeed completely?
- **Check:** Visit the exact URL Vercel provided

### "Can't find module"
- **Check:** All dependencies are in `frontend/package.json`
- **Redeploy:** Go to Deployments → Three dots → Redeploy

---

## Next Steps

✅ Frontend is live on Vercel!  
⏭️ Now deploy the backend: See **BACKEND_DEPLOYMENT.md**  
🔗 Then connect them by updating `NEXT_PUBLIC_API_URL`
