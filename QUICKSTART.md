# ⚡ Quick Start Guide

## 🚀 Start Locally (60 seconds)

```bash
# 1. Navigate to project
cd c:\Users\urbin\NewsApp

# 2. Create virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

✅ App opens at: http://localhost:8501

---

## 📦 Deploy to Railway (2 minutes)

### Step 1: Push to GitHub
```bash
cd c:\Users\urbin\NewsApp
git init
git config user.name "Your Name"
git config user.email "your@email.com"
git add .
git commit -m "Initial: Institutional News Scanner"
git branch -M main
git remote add origin https://github.com/ozytarget/news.git
git push -u origin main
```

### Step 2: Deploy via Railway
1. Go to https://railway.app/dashboard
2. Click **New Project**
3. Select **Deploy from GitHub**
4. Choose `ozytarget/news`
5. Click **Deploy**
6. Wait 2-3 minutes ⏳
7. Click your deployment → View Live URL 🎉

---

## 🎯 What's Included

✅ **Institutional Keywords** (40+ terms)
- FOMC, Fed decisions, Treasury yields, Volatility, etc.

✅ **Smart Filtering**
- Bloomberg-style domain filtering
- Noise detection (spam keywords)
- Auto-fallback (strict → relaxed → failsafe)

✅ **Real-Time Analytics**
- Retail sentiment gauge
- Market volatility meter
- Live news feed (Google News RSS)

✅ **Production-Ready**
- Docker containerization
- Railway.app integration
- GitHub Actions CI/CD

---

## 📊 Features

| Feature | Status |
|---------|--------|
| Auto-refresh (40s) | ✅ |
| Institutional filtering | ✅ |
| 5-level auto-fallback | ✅ |
| Sentiment analysis | ✅ |
| Dark theme | ✅ |
| Mobile responsive | ✅ |
| Error recovery | ✅ |

---

## 🔧 Customize

### Change Keywords
Edit `app.py` line ~40:
```python
INSTITUTIONAL_KEYWORDS = {'your_term': 10, ...}
```

### Change Refresh Speed
Edit `app.py` line ~390:
```python
auto(seconds=30)  # Faster refresh
```

### Change Domain Filters
Edit `app.py` line ~15:
```python
DOMAIN_ALLOWLIST = {'your.domain', ...}
```

---

## ❓ Troubleshooting

**Q: App won't start locally**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Q: Railway deployment fails**
- Check GitHub commit was pushed
- Railway should auto-detect `Dockerfile`
- Check Railway logs for errors

**Q: No news appearing**
- Google News RSS may rate-limit
- Auto-fallback to less strict filters (automatic)
- Wait 40 seconds for refresh

**Q: Can't push to GitHub**
```bash
# Verify credentials
git config user.name "Your Name"
git config user.email "your@email.com"
```

---

## 📚 Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Railway Docs**: https://docs.railway.app/
- **GitHub Docs**: https://docs.github.com/
- **Issues**: https://github.com/ozytarget/news/issues

---

## 💡 Pro Tips

1. **Local Development**: Edit `app.py` and refresh browser (Ctrl+R) - Streamlit auto-reloads
2. **Fast Testing**: Add keywords to `INSTITUTIONAL_KEYWORDS` to test filtering
3. **Monitor Railway**: Watch live logs in Railway dashboard while app runs
4. **Custom Domain**: Use Railway custom domain feature (paid feature)

---

**Made with ❤️ for Bloomberg-style institutional traders**
