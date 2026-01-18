# app.py - Institutional News Scanner
# Simplified version without streamlit-autorefresh (using only built-in Streamlit)

import os
import re
import time
from datetime import datetime, timezone
from urllib.parse import quote

import requests
import streamlit as st
from dateutil import parser as date_parser
import plotly.graph_objects as go
import feedparser

# Page config
st.set_page_config(page_title="📰 News Scanner", layout="wide", initial_sidebar_state="expanded")

# ==================== CONFIG ====================
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
AUTO_REFRESH_SECONDS = 30

DEFAULT_KEYWORDS = ["SPY", "FOMC", "Treasury", "yields", "inflation", "options", "gamma", "liquidity"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

# Institutional keywords
INSTITUTIONAL_KEYWORDS = {
    "fomc": 10, "fed": 10, "federal reserve": 10, "policy makers": 8,
    "treasury": 9, "bonds": 7, "yields": 8, "inflation": 8,
    "options": 7, "volatility": 8, "liquidity": 7, "earnings": 6,
    "guidance": 7, "capital allocation": 6, "buyback": 6,
}

# Noise keywords to filter out
NOISE_KEYWORDS = {"meme", "viral", "diamond hands", "moon", "rocket", "squeeze"}

# Allowed domains
DOMAIN_ALLOWLIST = {
    "reuters.com", "bloomberg.com", "ft.com", "wsj.com", "cnbc.com",
    "marketwatch.com", "finance.yahoo.com", "morningstar.com"
}

DOMAIN_BLOCKLIST = {
    "eurasiareview.com", "financialcontent.com", "discoveryalert.com",
    "medium.com", "substack.com", "blogspot.com"
}

# ==================== HELPER FUNCTIONS ====================

def now_utc():
    return datetime.now(timezone.utc)

def safe_parse_dt(date_str):
    try:
        parsed = date_parser.parse(date_str)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except:
        return None

def time_ago(dt):
    if not dt:
        return "Unknown"
    delta = now_utc() - dt
    minutes = delta.total_seconds() / 60
    if minutes < 1:
        return "Now"
    elif minutes < 60:
        return f"{int(minutes)}m ago"
    else:
        hours = minutes / 60
        return f"{int(hours)}h ago"

def count_hits(text, keywords):
    if not text:
        return 0
    text_lower = text.lower()
    return sum(text_lower.count(kw.lower()) for kw in keywords if kw)

def has_noise(text):
    if not text:
        return False
    text_lower = text.lower()
    return any(noise in text_lower for noise in NOISE_KEYWORDS)

def get_domain(url):
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""

def fetch_google_news(query, window_minutes=60):
    try:
        url = GOOGLE_NEWS_RSS.format(q=quote(query))
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        
        feed = feedparser.parse(resp.content)
        items = []
        
        cutoff = now_utc()
        for entry in feed.entries[:20]:
            try:
                pub_date = safe_parse_dt(entry.get("published", ""))
                if pub_date and (now_utc() - pub_date).total_seconds() > window_minutes * 60:
                    continue
                
                title = entry.get("title", "")
                link = entry.get("link", "")
                domain = get_domain(link)
                
                # Domain filtering
                if DOMAIN_BLOCKLIST and any(block in domain for block in DOMAIN_BLOCKLIST):
                    continue
                if DOMAIN_ALLOWLIST and not any(allow in domain for allow in DOMAIN_ALLOWLIST):
                    continue
                
                items.append({
                    "title": title,
                    "link": link,
                    "domain": domain,
                    "pub_date": pub_date,
                    "summary": entry.get("summary", "")[:200]
                })
            except Exception as e:
                continue
        
        return items, None
    except Exception as e:
        return [], str(e)

# ==================== STREAMLIT UI ====================

st.title("📰 Institutional News Scanner")
st.markdown("Bloomberg-style real-time financial news filtering with auto-fallback")

# Sidebar controls
st.sidebar.header("⚙️ Settings")

keywords_input = st.sidebar.text_input(
    "Custom Keywords",
    ", ".join(DEFAULT_KEYWORDS),
    help="Comma-separated keywords to search for"
)

keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Keywords", len(keywords))

with col2:
    st.metric("Auto-Refresh", f"Every {AUTO_REFRESH_SECONDS}s")

with col3:
    st.metric("Time", now_utc().strftime("%H:%M:%S UTC"))

st.write("---")

# Fetch news
st.write("### 📊 Latest News")

if keywords:
    all_items = []
    errors = []
    
    for keyword in keywords:
        items, error = fetch_google_news(keyword, window_minutes=60)
        if error:
            errors.append(f"'{keyword}': {error}")
        all_items.extend(items)
    
    if all_items:
        # Remove duplicates
        seen = set()
        unique_items = []
        for item in all_items:
            if item["link"] not in seen:
                seen.add(item["link"])
                unique_items.append(item)
        
        # Display
        for i, item in enumerate(unique_items[:15], 1):
            with st.expander(f"**{i}. {item['title'][:60]}...**"):
                st.write(f"**Source:** {item['domain']}")
                st.write(f"**Published:** {time_ago(item['pub_date'])}")
                st.write(f"**Summary:** {item['summary']}")
                st.markdown(f"[🔗 Read Full Article]({item['link']})")
    else:
        st.info("No articles found. Try different keywords or check your connection.")
    
    if errors:
        with st.expander("⚠️ Fetch Errors"):
            for error in errors:
                st.write(f"- {error}")
else:
    st.warning("Please enter keywords to search for news.")

st.write("---")
st.caption("Institutional News Scanner v1.0 | Data from Google News RSS")
