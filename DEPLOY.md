# Institutional News Scanner — Deployment Guide

## Quick Start

### GitHub Setup
```bash
cd c:\Users\urbin\NewsApp
git init
git config user.name "Ozy"
git config user.email "your@email.com"
git add .
git commit -m "Initial: Institutional News Scanner - AUTO"
git branch -M main
git remote add origin https://github.com/ozytarget/news.git
git push -u origin main
```

### Railway Deployment

1. **Connect Repository**
   - Go to railway.app → New Project
   - Select "Deploy from GitHub"
   - Choose `ozytarget/news`

2. **Automatic Detection**
   - Railway auto-detects `Dockerfile` ✓
   - Reads `railway.toml` configuration ✓
   - Installs from `requirements.txt` ✓

3. **Custom Domain (Optional)**
   - Railway → Project Settings
   - Add custom domain: `news.yourdomain.com`

## Project Structure

```
news/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image (Railway)
├── railway.toml          # Railway configuration
├── README.md             # Documentation
├── LICENSE               # MIT License
└── .gitignore            # Git ignore rules
```

## What's Included

✅ **app.py** (417 lines)
  - Auto-refresh every 40s
  - 40+ institutional keywords
  - 5-level auto-fallback system
  - Market sentiment analysis

✅ **requirements.txt**
  - streamlit>=1.28.0
  - streamlit-autorefresh>=0.4.0
  - feedparser, requests, pandas, plotly, numpy
  - python-dateutil

✅ **Dockerfile**
  - Python 3.11 slim image
  - Streamlit server configuration
  - Port 8501 exposed
  - Auto-generated .streamlit/config.toml

✅ **railway.toml**
  - Dockerfile build configuration
  - Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
  - Restart policy on failure

## Features Ready for Production

- ✅ Auto-refresh no sleep loops
- ✅ Auto-fallback (strict → relaxed)
- ✅ Bloomberg-style filtering
- ✅ Hidden "Sensitive Mode" for advanced users
- ✅ Multi-feed support (Google News primary)
- ✅ Real-time sentiment gauges
- ✅ Error handling & diagnostics
- ✅ Responsive dark theme
- ✅ Zero API keys required

## Deployment Commands

### Test Locally
```bash
streamlit run app.py
```

### Docker Test
```bash
docker build -t news:latest .
docker run -p 8501:8501 news:latest
```

### Push to GitHub
```bash
git add -A
git commit -m "Update: feature description"
git push origin main
```

### Monitor Railway Deployment
- Dashboard: https://railway.app
- Logs: `railway logs` (CLI)
- Metrics: CPU, Memory, Network

## Customization Post-Deploy

Edit `app.py` on GitHub and Railway auto-redeploys:

1. Change keywords: `INSTITUTIONAL_KEYWORDS`
2. Adjust refresh: `AUTO_REFRESH_SECONDS`
3. Modify fallback levels: `build_fallback_modes()`
4. Update sentiment logic: `calculate_sentiment()`

## Support & Issues

- **GitHub Issues**: https://github.com/ozytarget/news/issues
- **Railway Support**: https://railway.app/support
- **Streamlit Docs**: https://docs.streamlit.io

---

**Deployed with ❤️ by Ozy | © 2026**
