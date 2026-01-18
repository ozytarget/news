# 📁 Project Structure & Deployment Guide

## Local Project Structure

```
NewsApp/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container image definition
├── railway.toml                    # Railway deployment config
├── .gitignore                      # Git ignore rules
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── .github/
│   └── workflows/
│       └── build.yml              # GitHub Actions CI/CD
├── README.md                       # Main documentation
├── DEPLOY.md                       # Deployment guide
├── CONFIG.md                       # Configuration options
├── QUICKSTART.md                   # Quick start guide
├── CONTRIBUTING.md                 # Contributing guidelines
└── LICENSE                         # MIT License
```

## Files Overview

### Core Application
- **app.py** (417 lines)
  - Main Streamlit app
  - News fetching from Google News RSS
  - Institutional keyword filtering
  - 5-level auto-fallback system
  - Sentiment analysis

### Configuration Files
- **requirements.txt** - Python dependencies (8 packages)
- **Dockerfile** - Docker image for Railway (Python 3.11 slim)
- **railway.toml** - Railway.app deployment config
- **.streamlit/config.toml** - Streamlit theme & settings
- **.gitignore** - Files to exclude from Git

### Documentation
- **README.md** - Complete project documentation
- **QUICKSTART.md** - 60-second setup guide
- **DEPLOY.md** - Deployment instructions
- **CONFIG.md** - Configuration & troubleshooting
- **CONTRIBUTING.md** - Contribution guidelines

### CI/CD
- **.github/workflows/build.yml** - Automated testing on GitHub

### Legal
- **LICENSE** - MIT License

## Deployment Flow

```
Local Development
    ↓
Git Commit & Push to GitHub
    ↓
GitHub Creates Repository
    ↓
Railway Detects Repository
    ↓
Railway Builds Docker Image
    ↓
Railway Deploys Container
    ↓
Live at: https://your-project.railway.app
```

## Step-by-Step Deployment

### Step 1: Prepare Local Repository

```bash
cd c:\Users\urbin\NewsApp

# Initialize Git
git init

# Configure user (replace with your info)
git config user.name "Ozy"
git config user.email "your@email.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial: Institutional News Scanner - Bloomberg-style filtering with auto-fallback"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `news`
3. Description: "Institutional news scanner with Bloomberg-style filtering"
4. **DO NOT** initialize with README (we already have one)
5. Click **Create repository**

### Step 3: Push to GitHub

```bash
# Set main branch
git branch -M main

# Add remote
git remote add origin https://github.com/ozytarget/news.git

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy to Railway

1. Go to https://railway.app/dashboard
2. Click **New Project**
3. Select **Deploy from GitHub**
4. Authorize GitHub account (first time only)
5. Select `ozytarget/news` repository
6. Railway auto-detects:
   - ✅ `Dockerfile` → builds image
   - ✅ `railway.toml` → configuration
   - ✅ `requirements.txt` → dependencies
7. Click **Deploy**
8. Wait 2-3 minutes for build ⏳
9. Click deployment → **View Live URL**

### Step 5: Verify Deployment

- ✅ App loads without errors
- ✅ News articles appear
- ✅ Filtering works
- ✅ Auto-refresh functions (40 seconds)
- ✅ Sentiment gauges display

## Key Deployment Files Explained

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Why this setup:**
- `python:3.11-slim` - Lightweight base image
- `--no-cache-dir` - Smaller image size
- `EXPOSE 8501` - Streamlit port
- `--server.address=0.0.0.0` - Listen on all interfaces

### railway.toml

```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

**Why this setup:**
- `builder = "dockerfile"` - Use Dockerfile for build
- `$PORT` - Railway's dynamic port variable
- `on_failure` with retries - Auto-restart on crash

## Environment Variables (Railway)

Railway automatically provides:
- `$PORT` - Dynamic port (default 8501)
- `$RAILWAY_ENVIRONMENT_ID` - Deployment environment
- `$RAILWAY_RUN_UID` - Unique run identifier

To add custom variables in Railway:
1. Go to project → Variables
2. Add key-value pairs
3. Variables available to app.py via `os.getenv('KEY')`

## Git Workflow After Deployment

### Make Changes Locally

```bash
# Make edits to app.py or other files
# ... edit files ...

# Stage changes
git add .

# Commit
git commit -m "Fix: Updated sentiment analysis thresholds"

# Push to GitHub
git push origin main
```

### Railway Auto-Redeploys

1. GitHub receives push
2. Railway webhook triggers
3. New Docker image built
4. New container deployed
5. Old container stopped
6. Live app updated ✅

Typical deployment time: **90-120 seconds**

## Monitoring Deployment

### In Railway Dashboard

1. Select your project
2. Click deployment
3. Monitor tabs:
   - **Logs** - Real-time output
   - **Metrics** - CPU/Memory usage
   - **Deployments** - Deployment history
   - **Settings** - Configuration

### Common Issues

| Issue | Solution |
|-------|----------|
| Build fails | Check Dockerfile syntax, run `docker build .` locally |
| App crashes | Check logs, look for missing imports in requirements.txt |
| No news loading | Check Google News RSS connectivity, verify filters |
| Port errors | Railway auto-assigns $PORT, should not hardcode 8501 |

## Updating Project

### Add New Dependency

1. Locally: `pip install new_package`
2. Update: `pip freeze > requirements.txt`
3. Git: 
   ```bash
   git add requirements.txt
   git commit -m "Add: new_package v1.2.3"
   git push
   ```
4. Railway auto-redeploys

### Update Code

1. Edit `app.py` or other files
2. Test locally: `streamlit run app.py`
3. Git:
   ```bash
   git add .
   git commit -m "Feature: description"
   git push
   ```
4. Railway auto-redeploys

## Troubleshooting Deployment

### Railway Can't Find Dockerfile

**Solution:** Ensure `.dockerignore` and `Dockerfile` in root directory
```bash
ls -la  # Should see Dockerfile in list
```

### Python Version Error

**Solution:** Dockerfile specifies Python 3.11
- Edit `Dockerfile` line 1: `FROM python:3.11-slim`
- Commit and push
- Railway rebuilds

### Missing Module Error

**Solution:** Add to `requirements.txt`
```bash
pip install missing_module
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Fix: add missing_module"
git push
```

### App Restarts Constantly

**Solution:** Check Railway logs
1. Go to Railway dashboard
2. Click Logs tab
3. Look for error messages
4. Fix in app.py, commit, push

## Production Checklist

- [ ] `app.py` tested locally
- [ ] All imports in `requirements.txt`
- [ ] `Dockerfile` builds successfully: `docker build .`
- [ ] No hardcoded secrets in code
- [ ] `railway.toml` configured correctly
- [ ] README updated with any custom changes
- [ ] GitHub repository created
- [ ] Code pushed to `main` branch
- [ ] Railway project created
- [ ] Deployment successful (5 min wait)
- [ ] Live URL accessible
- [ ] Auto-refresh working
- [ ] News loading (with fallback)

## Next Steps

1. ✅ **Local Setup** - Follow QUICKSTART.md
2. ✅ **GitHub Push** - Use git commands above
3. ✅ **Railway Deploy** - Use Railway dashboard
4. 📊 **Monitor** - Watch Railway logs
5. 🎉 **Share** - Share your live URL!

---

**Questions?** Check [CONFIG.md](CONFIG.md) or [QUICKSTART.md](QUICKSTART.md)
