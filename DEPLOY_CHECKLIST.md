# 🚀 Deployment Checklist & Commands

## Pre-Deployment Verification ✅

```bash
# 1. Test app locally
streamlit run app.py
# Expected: Opens http://localhost:8501, no errors

# 2. Verify dependencies
pip install -r requirements.txt
# Expected: All packages install successfully

# 3. Check Docker locally (optional)
docker build -t news-scanner:test .
# Expected: Build completes successfully
```

---

## GitHub Push Commands 📤

Copy-paste these commands in PowerShell:

```powershell
# Navigate to project
cd c:\Users\urbin\NewsApp

# 1. Initialize Git repository
git init

# 2. Configure Git user (change name/email to yours)
git config user.name "Ozy"
git config user.email "your-email@example.com"

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Institutional News Scanner with Bloomberg-style filtering"

# 5. Rename branch to main
git branch -M main

# 6. Add GitHub remote (https://github.com/ozytarget/news)
git remote add origin https://github.com/ozytarget/news.git

# 7. Push to GitHub
git push -u origin main
```

**Expected Output:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX)
...
* [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## GitHub Repository Setup 🐙

If you haven't created the repository yet:

1. Go to https://github.com/new
2. Fill in form:
   - **Repository name**: `news`
   - **Description**: `Institutional news scanner with Bloomberg-style filtering and auto-fallback`
   - **Public/Private**: Public (recommended)
   - **Initialize with**: None (we have README)
3. Click **Create repository**
4. Run push commands above ☝️

---

## Railway Deployment 🚄

### Step 1: Connect Railway & GitHub

1. Go to https://railway.app/dashboard
2. Click **New Project**
3. Select **Deploy from GitHub**
4. Click **Authorize** (first time only)
5. Select repository:
   - Find: `ozytarget/news`
   - Click to select
6. Railway auto-detects:
   - ✅ `Dockerfile`
   - ✅ `railway.toml`
   - ✅ `requirements.txt`

### Step 2: Configure (Usually Auto)

Railway should auto-detect everything. If manual config needed:

**Environment Variables** (usually not needed):
- `STREAMLIT_SERVER_PORT`: Already set in Dockerfile
- `STREAMLIT_SERVER_ADDRESS`: Already set to 0.0.0.0

### Step 3: Deploy

1. Click **Deploy** button
2. Railway starts building:
   - ⏳ Builds Docker image (1-2 min)
   - ⏳ Deploys container (30-60 sec)
   - ✅ Shows "Deployed" when complete

### Step 4: Access Live App

1. Railway shows deployment details
2. Click on deployment box
3. Click **View Live URL**
4. Opens your live app! 🎉

---

## Post-Deployment Verification ✅

After deployment, verify:

```
✅ App loads without errors
✅ News articles display
✅ "Institutional Keywords" filter working
✅ "Fallback Mode" shows as "STRICT"
✅ Auto-refresh working (40s intervals)
✅ Sentiment gauges display values
✅ No error messages in Railway logs
```

### Check Railway Logs

1. Railway dashboard → Select deployment
2. Click **Logs** tab
3. Should see:
   ```
   Streamlit server is running
   Local URL: http://localhost:8501
   Network URL: http://0.0.0.0:8501
   ```

---

## Updating Code After Deployment 🔄

Once live on Railway, updates are automatic:

```powershell
# 1. Make changes to app.py (or other files)
# ... edit files in VS Code ...

# 2. Stage & commit changes
git add .
git commit -m "Feature: description of change"

# 3. Push to GitHub
git push origin main

# 4. Railway automatically:
#    - Detects push via GitHub webhook
#    - Rebuilds Docker image
#    - Deploys new container
#    - Updates live app
# Time: ~90-120 seconds
```

---

## Troubleshooting 🔧

### GitHub Push Fails

**Error**: `fatal: not a git repository`
```powershell
# Solution: Run from project directory
cd c:\Users\urbin\NewsApp
git init
```

**Error**: `authentication failed`
```powershell
# Solution 1: Use GitHub token (recommended)
# Solution 2: Check user.name and user.email configured
git config user.name  # Should return name
git config user.email # Should return email
```

**Error**: `branch 'main' set up to track...`
```powershell
# This is normal output, not an error
# Just means your branch is tracking remote
```

### Railway Deployment Fails

**Build fails**: `No Dockerfile found`
- Verify `Dockerfile` exists in root: `ls -la Dockerfile`
- Verify `Dockerfile` name is exact (capital D)

**App crashes**: `ModuleNotFoundError`
- Add missing package to `requirements.txt`
- Run: `pip install missing_package`
- Run: `pip freeze > requirements.txt`
- Commit and push to GitHub
- Railway auto-rebuilds

**No news showing**: 
- Google News may rate-limit
- Auto-fallback to less strict filter (automatic)
- Check Railway logs for errors
- Wait 40 seconds for auto-refresh

**Port conflicts**:
- Railway uses dynamic `$PORT` variable
- Should work automatically
- Don't hardcode 8501

### Local Testing Issues

**Error**: `ModuleNotFoundError: No module named 'streamlit'`
```powershell
pip install -r requirements.txt
```

**Error**: `Address already in use`
```powershell
# Kill existing Streamlit process
Get-Process streamlit | Stop-Process
```

---

## Quick Reference Commands 📝

```powershell
# Git commands
git init                                    # Initialize repository
git add .                                  # Stage all files
git commit -m "message"                   # Commit with message
git branch -M main                        # Rename to main
git remote add origin URL                 # Add GitHub repository
git push -u origin main                   # Push to GitHub
git log --oneline                         # View commit history
git status                                # Check changes

# Python commands
python -m venv .venv                      # Create virtual environment
.venv\Scripts\activate                    # Activate venv (Windows)
pip install -r requirements.txt           # Install dependencies
pip freeze > requirements.txt             # Update requirements
streamlit run app.py                      # Run app locally

# Docker commands (optional)
docker build -t news-scanner .            # Build image locally
docker run -p 8501:8501 news-scanner     # Run container locally
```

---

## File Checklist ✅

Before GitHub push, verify these files exist:

```
✅ app.py                          (417 lines)
✅ requirements.txt                (8 packages)
✅ Dockerfile                      (Docker config)
✅ railway.toml                    (Railway config)
✅ .gitignore                      (Git rules)
✅ .dockerignore                   (Docker build optimization)
✅ .streamlit/config.toml          (Streamlit theme)
✅ .github/workflows/build.yml     (CI/CD)
✅ README.md                       (Main documentation)
✅ QUICKSTART.md                   (60-second guide)
✅ DEPLOY.md                       (Deployment guide)
✅ CONFIG.md                       (Configuration)
✅ STRUCTURE.md                    (File structure)
✅ CONTRIBUTING.md                 (Contributing guide)
✅ CHANGELOG.md                    (Version history)
✅ LICENSE                         (MIT license)
```

---

## Success Indicators 🎉

✅ **GitHub Push Successful When:**
- Repository appears on https://github.com/ozytarget/news
- All files visible in GitHub
- Main branch selected

✅ **Railway Deployment Successful When:**
- Railway shows "Deployed" status
- Live URL accessible
- App loads without errors
- News articles display
- Auto-refresh works (40s)

---

## Need Help? 🆘

1. **GitHub errors**: Check [STRUCTURE.md](STRUCTURE.md#troubleshooting-deployment)
2. **Railway errors**: Check Railway dashboard logs
3. **Code issues**: Check [README.md](README.md) FAQ
4. **Configuration**: See [CONFIG.md](CONFIG.md)
5. **Quick help**: See [QUICKSTART.md](QUICKSTART.md)

---

## Next Steps 🚀

1. ✅ Run local tests
2. ✅ Push to GitHub (use commands above)
3. ✅ Deploy to Railway (use steps above)
4. ✅ Share live URL with team
5. ✅ Monitor live app
6. ✅ Make improvements

---

**Estimated Total Time: 10-15 minutes** ⏱️

Good luck with your deployment! 🚀
