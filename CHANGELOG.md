# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2024

### ✨ Features
- **Institutional News Scanner**: Bloomberg-style financial news filtering
- **40+ Institutional Keywords**: FOMC, Fed decisions, treasury yields, volatility, etc.
- **5-Level Auto-Fallback System**: 
  - STRICT (10 min window, strict filtering)
  - RELAX 1-3 (progressive relaxation)
  - FAILSAFE (240 min window, maximum coverage)
- **Domain Filtering**: Allowlist/blocklist for reliable sources
- **Noise Detection**: Filters spam keywords (meme, viral, diamond hands, etc.)
- **Real-Time Sentiment Analysis**: 
  - Retail sentiment gauge
  - Market volatility meter
- **Auto-Refresh**: Updates every 40 seconds
- **Dark Theme UI**: Bloomberg-style dark interface

### 🏗️ Infrastructure
- **Streamlit Application**: Real-time web interface
- **Google News RSS Integration**: Primary news source
- **Docker Containerization**: Python 3.11 slim base image
- **Railway Deployment**: One-click deployment from GitHub
- **GitHub Actions CI/CD**: Automated testing on push/PR
- **Error Recovery**: Graceful fallback when news unavailable

### 📦 Dependencies
- streamlit >= 1.28.0
- streamlit-autorefresh >= 0.4.0
- feedparser >= 6.0.10
- requests >= 2.31.0
- pandas >= 2.1.0
- numpy >= 1.24.0
- python-dateutil >= 2.8.2
- plotly >= 5.17.0

### 📚 Documentation
- Comprehensive README.md
- Quick start guide (QUICKSTART.md)
- Deployment guide (DEPLOY.md)
- Configuration guide (CONFIG.md)
- Project structure guide (STRUCTURE.md)
- Contributing guidelines (CONTRIBUTING.md)

### 🔧 Configuration
- Streamlit config: `.streamlit/config.toml`
- Railway config: `railway.toml`
- GitHub Actions: `.github/workflows/build.yml`
- Docker optimization: `.dockerignore`
- Git rules: `.gitignore`

### 🐛 Bug Fixes
- ✅ Fixed indentation errors
- ✅ Fixed NameError exceptions
- ✅ Disabled problematic RSS feeds (Reuters, CNBC)
- ✅ Improved error handling
- ✅ Added graceful fallback mechanism

---

## Release Notes

### v1.0.0 - Initial Release
- Full institutional news scanner with auto-fallback
- Production-ready Docker/Railway deployment
- Complete documentation suite
- GitHub Actions CI/CD pipeline

---

## Roadmap (Future Features)

- [ ] Custom keyword weighting per user
- [ ] Email/Slack notifications
- [ ] Historical data analysis
- [ ] News archive search
- [ ] API endpoint for external integration
- [ ] Custom theme support
- [ ] Multi-language support
- [ ] Advanced sentiment NLP (transformers)
- [ ] Portfolio-specific news filtering
- [ ] Trading signal integration

---

## Migration Guide

### From Manual RSS Feeds to Google News API

**Why**: Direct RSS feeds (Reuters, CNBC, Bloomberg) were unreliable.
**Change**: Switched to Google News RSS + 5-level auto-fallback.
**Impact**: More stable, but results may vary slightly.

### Updating to Latest Version

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Test locally
streamlit run app.py

# Push to Railway (if using)
git add .
git commit -m "Update to v1.0.0"
git push origin main
```

---

## Support

- **GitHub Issues**: https://github.com/ozytarget/news/issues
- **GitHub Discussions**: https://github.com/ozytarget/news/discussions
- **Documentation**: See README.md and guides

---

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2024 | Stable | Production release |

---

**Last Updated**: 2024
