# 📰 Institutional News Scanner — AUTO

**Automated institutional news scanner with Bloomberg-style filtering & auto-fallback mode**

## Features

✅ **Auto-Refresh Every 40 Seconds** - No manual intervention needed  
✅ **Institutional Keywords Filtering** - 40+ Bloomberg-style finance terms  
✅ **Auto-Fallback Modes** - Starts strict (10m), relaxes if zero results  
✅ **Noise Detection** - Filters out memes, viral spam, social media hype  
✅ **Domain Filtering** - Allowlist (Reuters, Bloomberg, FT, WSJ, etc.) & blocklist  
✅ **Live Market Sentiment** - Real-time retail + volatility sentiment gauges  
✅ **Multi-Feed Support** - Google News RSS (primary)  
✅ **No API Keys Required** - Works without Bloomberg/Reuters APIs  

## Installation

### Local Setup

```bash
git clone https://github.com/ozytarget/news.git
cd news
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open browser: http://localhost:8501

### Docker Setup

```bash
docker build -t news-scanner .
docker run -p 8501:8501 news-scanner
```

## Deploy to Railway

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Institutional News Scanner"
git branch -M main
git remote add origin https://github.com/ozytarget/news.git
git push -u origin main
```

### 2. Deploy on Railway
- Go to [Railway.com](https://railway.app/)
- Click "New Project" → "Deploy from GitHub"
- Select `ozytarget/news` repository
- Railway auto-detects Dockerfile
- Click "Deploy"

**Live URL**: `https://your-project.railway.app`

## Configuration

### Sensitive Mode (Hidden Settings)
- Toggle "Sensitive Mode" in sidebar
- Adjust: Base window (minutes), filter thresholds

### Keywords
Edit `INSTITUTIONAL_KEYWORDS` in `app.py` to customize

### Filter Allowlist/Blocklist
Modify `DOMAIN_ALLOWLIST` and `DOMAIN_BLOCKLIST` constants

## Architecture

```
app.py
├── fetch_google_news()      → Google News RSS
├── fetch_rss_feed()         → Direct RSS (optional)
├── apply_filters()          → Bloomberg-style filters
├── build_fallback_modes()   → 5-level auto-relax
└── sentiment_analysis()     → Market sentiment gauges
```

## API Reference

### FallbackMode Dataclass
```python
@dataclass
class FallbackMode:
    name: str
    window_minutes: int
    min_kw: int          # Minimum institutional keywords
    max_noise: int       # Maximum noise keywords allowed
    allowlist_only: bool # Use domain allowlist only
```

### Fallback Levels (Automatic)
1. **STRICT 10m** - 10 min window, min 2 kw, allowlist ON
2. **RELAX 1 30m** - 30 min window, min 1 kw, allowlist ON
3. **RELAX 2 60m** - 60 min window, min 1 kw, allowlist OFF
4. **RELAX 3 120m** - 120 min window, min 0 kw, noise ≤ 1
5. **FAILSAFE 240m** - 240 min window, min 0 kw, noise ≤ 2

## Performance

- **Response Time**: < 2s (Google News RSS)
- **Refresh Interval**: 40 seconds
- **Max Headlines**: 40 per refresh
- **Memory**: ~150 MB (single instance)

## Troubleshooting

### No Headlines Appearing
1. Check "Feed errors" expandable section
2. Verify internet connectivity
3. Check Google News RSS endpoint (may be rate-limited)
4. Increase base window minutes in Sensitive Mode

### High CPU Usage
- Streamlit auto-refresh can be resource-intensive
- Consider increasing refresh interval in `AUTO_REFRESH_SECONDS`

### Railway Deploy Stuck
- Check railway.app logs: `railway logs`
- Verify Dockerfile builds locally: `docker build -t test .`
- Check start command in `railway.toml`

## Environment Variables (Railway)

No API keys required. Optional:

```bash
# Future: Bing News API (if enabled)
BING_NEWS_API_KEY=your_key
```

## License

MIT License - See LICENSE file

## Author

**Ozy** — © 2026

---

**Questions?** Open an issue on GitHub: https://github.com/ozytarget/news/issues
