# Institutional News Scanner - Configuration Guide

## Environment Variables (Optional)

Create a `.env` file in the project root for local development:

```env
# Auto-refresh interval in seconds (default: 40)
REFRESH_SECONDS=40

# Log level
LOG_LEVEL=INFO
```

## Docker Configuration

### Build Locally
```bash
docker build -t news-scanner:latest .
docker run -p 8501:8501 news-scanner:latest
```

### Docker Environment Variables
```bash
docker run -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  news-scanner:latest
```

## Railway Deployment Troubleshooting

### Error: "No logs in Railway"
- Check app.py for syntax errors
- Verify all imports are in requirements.txt
- Ensure Dockerfile is valid

### Error: "Connection refused"
- Check port 8501 is exposed in Dockerfile
- Verify `--server.address=0.0.0.0` in startCommand
- Check `EXPOSE 8501` in Dockerfile

### Error: "Module not found"
- Add missing package to requirements.txt
- Push to GitHub
- Railway will auto-redeploy

### Error: "RSS Feed not loading"
- Check network connectivity
- Google News RSS endpoint may be rate-limited
- Fallback modes activate automatically

## Customization

### Change Institutional Keywords

Edit `app.py`:
```python
INSTITUTIONAL_KEYWORDS = {
    'your_keyword': 10,  # Score weight
    'another_term': 5,
}
```

### Change Domain Filters

```python
DOMAIN_ALLOWLIST = {
    'yourdomain.com',
    'anotherdomain.com',
}

DOMAIN_BLOCKLIST = {
    'spam.com',
    'blocked.com',
}
```

### Change Auto-Refresh Interval

In `app.py`, modify:
```python
auto(seconds=YOUR_SECONDS)  # Change from 40
```

### Add Custom News Sources

Replace `fetch_google_news()` with:
```python
def fetch_rss_feed(url):
    # Implement RSS fetching logic
    pass
```

## Production Checklist

- [ ] All dependencies in requirements.txt
- [ ] No hardcoded secrets in code
- [ ] Tests pass locally
- [ ] Dockerfile builds successfully
- [ ] README is up to date
- [ ] CHANGELOG updated for new features
- [ ] Git branch merged to main
- [ ] Railway deployment successful
- [ ] Live URL accessible

## Monitoring

### Railway Dashboard
1. Go to https://railway.app
2. Select your project
3. Monitor:
   - Logs (real-time output)
   - Metrics (CPU, Memory)
   - Deployments (history)

### Local Logs
```bash
# Follow Flask logs
streamlit run app.py --logger.level=debug
```

## Support

- **GitHub Issues**: https://github.com/ozytarget/news/issues
- **Railway Support**: https://railway.app/support
- **Streamlit Docs**: https://docs.streamlit.io/

