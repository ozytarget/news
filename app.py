# app.py
# Independent News Scanner (Google + Bing) with Auto Filters every 30 seconds
# - Runs standalone (no tabs required)
# - Auto refresh every 30s (no sleep loops)
# - Automatic institutional/noise filtering
# - Manual keyword override + auto scan keywords
#
# Install:
#   pip install streamlit streamlit-autorefresh feedparser requests pandas python-dateutil plotly
#
# Run:
#   streamlit run app.py

import os
import re
import time
from datetime import datetime, timezone
from urllib.parse import quote

import requests
import streamlit as st
from dateutil import parser as date_parser
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go


# =========================
# CONFIG
# =========================
AUTO_REFRESH_SECONDS = 30
DEFAULT_KEYWORDS = ["SPY", "FOMC", "Treasury", "yields", "inflation", "options", "gamma", "liquidity"]

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
BING_NEWS_ENDPOINT = "https://api.bing.microsoft.com/v7.0/news/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
}

# Set this environment variable:
#   BING_NEWS_API_KEY=your_key
BING_API_KEY = os.getenv("BING_NEWS_API_KEY", "").strip()

# Institutional and noise filters (Bloomberg-style) - EXPANDED
INSTITUTIONAL_KEYWORDS = [
    # ----------------------------
    # FED / CENTRAL BANKS
    # ----------------------------
    "fomc", "fed", "federal reserve", "policy makers", "rate path", "terminal rate",
    "restrictive", "accommodative", "forward guidance", "dot plot", "policy recalibration",
    "policy normalization", "balance sheet", "runoff", "qt", "qe", "inflation persistence",
    "labor market rebalancing", "ecb", "boj", "boe",

    # ----------------------------
    # TREASURY / RATES / BONDS
    # ----------------------------
    "treasury issuance", "treasury refunding", "refunding announcement", "issuance calendar",
    "auction results", "auction tail", "bid-to-cover", "weak demand", "strong demand",
    "curve steepening", "curve flattening", "curve repricing", "real yields", "real yield",
    "term premium", "duration risk", "supply overhang", "yields", "yield", "bonds", "debt ceiling",

    # ----------------------------
    # FLOWS / POSITIONING
    # ----------------------------
    "institutional positioning", "asset allocation", "asset allocation shift",
    "rebalancing flows", "portfolio reallocation", "reallocation flows", "portfolio rebalancing",
    "passive inflows", "etf inflows", "etf creations", "etf redemptions", "creations", "redemptions",
    "cta positioning", "risk parity", "risk parity adjustment", "volatility targeting",
    "volatility targeting funds", "systematic strategies",

    # ----------------------------
    # DERIVATIVES / OPTIONS
    # ----------------------------
    "dealer hedging", "dealer hedging activity", "gamma exposure", "negative gamma", "positive gamma",
    "options-related flows", "options related flows", "open interest", "open interest concentration",
    "strike concentration", "strike congestion", "expiration-driven volatility", "expiration driven volatility",
    "implied volatility", "implied volatility pricing", "skew steepening", "convexity hedging",

    # ----------------------------
    # RISK / LIQUIDITY / SYSTEM
    # ----------------------------
    "liquidity conditions", "funding stress", "market dislocation", "financial conditions",
    "financial conditions tightening", "financial conditions easing", "systemic risk",
    "deleveraging", "volatility spike", "risk-off", "risk off", "cross-asset volatility",
    "cross asset volatility", "global capital flows", "funding markets", "stress indicators",

    # ----------------------------
    # CORPORATE (HIGH SIGNAL)
    # ----------------------------
    "earnings outlook", "guidance", "guidance reaffirmed", "guidance withdrawn",
    "margin compression", "margin outlook", "cost pressures", "pricing power",
    "capital allocation", "buyback authorization", "debt refinancing", "credit downgrade",
    "outlook", "covenant pressure",

    # ----------------------------
    # GEOPOL (MARKET MOVING)
    # ----------------------------
    "sanctions enforcement", "trade restrictions", "tariffs", "supply-chain disruption",
    "supply chain disruption", "shipping route disruption", "shipping disruptions",
    "energy supply risk", "geopolitical risk premium", "fiscal sustainability", "sovereign risk",

    # ----------------------------
    # CRYPTO (INSTITUTIONAL)
    # ----------------------------
    "etf", "etf inflows", "institutional adoption", "spot market demand", "spot demand",
    "custody services", "regulatory clarity", "market structure", "exchange outflows",
    "bitcoin", "ethereum",

    # ----------------------------
    # BLOOMBERG QUALITY PHRASES
    # ----------------------------
    "said in a statement", "according to people familiar", "people familiar with the matter",
    "data showed", "markets repriced", "investors reassessed", "policy makers signaled",
    "traders priced in", "priced in",
]

NOISE_KEYWORDS = [
    "meme", "viral", "to the moon", "diamond hands", "paper hands",
    "social media", "influencer", "hype", "ape",
    "soars", "surges", "plunges", "rockets",
    "could", "might", "hopes",
]


# =========================
# UI
# =========================
st.set_page_config(page_title="Independent Institutional News Scanner", layout="wide")

st.markdown(
    """
<style>
.stApp { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); color: #e6edf3; }
.header { color: #79c0ff; font-size: 28px; font-weight: 800; letter-spacing: 1px; font-family: 'Courier New', monospace; }
.card { border-left: 3px solid #1f6feb; padding: 12px 14px; margin-bottom: 10px; background: rgba(20, 20, 30, 0.92); border-radius: 6px; }
.meta { color: #8b949e; font-size: 11px; }
.source { color: #79c0ff; font-size: 11px; font-weight: 700; margin-right: 10px; }
.title { color: #e6edf3; font-size: 13px; font-weight: 650; line-height: 1.35; }
.badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:10px; margin-left:6px; border:1px solid rgba(121,192,255,.25); color:#79c0ff; }
hr { border: 0; border-top: 1px solid rgba(255,255,255,.08); }
</style>
""",
    unsafe_allow_html=True,
)

# Auto-refresh tick (no blocking)
st_autorefresh(interval=AUTO_REFRESH_SECONDS * 1000, key="auto_refresh_tick")


# =========================
# STATE
# =========================
if "latest_news" not in st.session_state:
    st.session_state["latest_news"] = []
if "last_fetch_ts" not in st.session_state:
    st.session_state["last_fetch_ts"] = 0.0
if "auto_keywords" not in st.session_state:
    st.session_state["auto_keywords"] = DEFAULT_KEYWORDS


# =========================
# HELPERS
# =========================
def safe_parse_time(value: str) -> float:
    if not value:
        return 0.0
    try:
        dt = date_parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:
        return 0.0


def time_ago(ts_seconds: float) -> str:
    now = time.time()
    diff = max(0, now - ts_seconds)
    if diff < 60:
        return f"{int(diff)}s"
    if diff < 3600:
        return f"{int(diff // 60)}m"
    return f"{int(diff // 3600)}h"


def count_hits(text: str, keywords: list[str]) -> int:
    s = (text or "").lower()
    return sum(1 for kw in keywords if kw in s)


def filter_institutional(items: list[dict], min_kw: int, max_noise: int) -> list[dict]:
    out = []
    for a in items:
        title = (a.get("title") or "").strip()
        if len(title) < 5:
            continue

        # Count hits on title + summary (if exists) for better signal
        blob = f"{title}\n{a.get('summary','')}".strip()

        kw_hits = count_hits(blob, INSTITUTIONAL_KEYWORDS)
        noise_hits = count_hits(blob, NOISE_KEYWORDS)

        if kw_hits >= min_kw and noise_hits <= max_noise:
            b = dict(a)
            b["_kw_hits"] = kw_hits
            b["_noise_hits"] = noise_hits
            out.append(b)
    return out


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for a in items:
        link = (a.get("link") or "").strip()
        if link:
            key = ("link", link)
        else:
            t = re.sub(r"\s+", " ", (a.get("title") or "").strip().lower())
            key = ("title", t[:240])

        if key in seen:
            continue
        seen.add(key)
        out.append(a)
    return out


def sort_most_recent(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda x: x.get("_ts", 0.0), reverse=True)


def fetch_google_news(keywords: list[str]) -> list[dict]:
    q = quote(" OR ".join(keywords)) if keywords else quote("SPY")
    url = GOOGLE_NEWS_RSS.format(q=q)
    feed = requests.get(url, headers=HEADERS, timeout=12)
    feed.raise_for_status()

    import feedparser  # local import to keep deps explicit

    parsed = feedparser.parse(feed.content)
    items = []
    for e in parsed.entries[:50]:
        title = getattr(e, "title", "") or ""
        link = getattr(e, "link", "") or ""
        published = getattr(e, "published", "") or ""
        summary = getattr(e, "summary", "") or ""

        ts = safe_parse_time(published)
        items.append({
            "source": "GoogleNews",
            "title": title.strip(),
            "link": link.strip(),
            "time": published.strip(),
            "summary": summary.strip(),
            "_ts": ts,
        })
    return items


def fetch_bing_news(keywords: list[str]) -> list[dict]:
    if not BING_API_KEY:
        return []

    query = " OR ".join(keywords) if keywords else "SPY"
    params = {
        "q": query,
        "mkt": "en-US",
        "count": 25,
        "sortBy": "Date",
        "freshness": "Day",
        "safeSearch": "Off",
        "textFormat": "Raw",
    }
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY, **HEADERS}
    r = requests.get(BING_NEWS_ENDPOINT, params=params, headers=headers, timeout=12)
    r.raise_for_status()
    data = r.json()

    items = []
    for v in data.get("value", [])[:25]:
        title = (v.get("name") or "").strip()
        link = (v.get("url") or "").strip()
        published = (v.get("datePublished") or "").strip()
        ts = safe_parse_time(published)
        items.append({
            "source": "BingNews",
            "title": title,
            "link": link,
            "time": published,
            "_ts": ts,
        })
    return items


def calculate_retail_sentiment(news: list[dict]) -> tuple[float, str]:
    bullish = ["beats", "surge", "rise", "gain", "record", "strong", "upgrade"]
    bearish = ["miss", "fall", "drop", "cut", "downgrade", "weak", "recession", "default"]
    score = 0
    for a in news:
        t = (a.get("title") or "").lower()
        score += sum(1 for w in bullish if w in t)
        score -= sum(1 for w in bearish if w in t)
    norm = 0.5 + max(-10, min(10, score)) / 20.0
    text = "Bullish" if norm > 0.55 else "Bearish" if norm < 0.45 else "Neutral"
    return norm, text


def calculate_volatility_sentiment(news: list[dict]) -> tuple[float, str]:
    risk_words = ["volatility", "turmoil", "selloff", "panic", "stress", "crisis", "risk-off", "spike"]
    hits = 0
    for a in news:
        t = (a.get("title") or "").lower()
        hits += sum(1 for w in risk_words if w in t)
    score = min(100.0, hits * 8.0)
    text = "Low" if score < 33 else "Elevated" if score < 66 else "High"
    return score, text


# =========================
# MAIN FEED (SHOW FIRST - MOST IMPORTANT)
# =========================

# Show the header and auto-fetch section first (before controls)
st.markdown('<div class="header">INDEPENDENT NEWS SCANNER — AUTO FILTERED</div>', unsafe_allow_html=True)

# FETCH NOW BUTTON AT THE TOP
col_fetch_top, col_spacer_top = st.columns([1, 3])
with col_fetch_top:
    if st.button("🔄 Fetch Now (Manual)", use_container_width=True, key="fetch_now_top"):
        st.session_state["last_fetch_ts"] = 0.0  # force immediate fetch

st.markdown("---")

news = st.session_state.get("latest_news") or []

if not news:
    st.info("📰 Loading news... Adjust settings below to customize your feed.")
else:
    st.subheader(f"📰 Latest Institutional Headlines ({len(news)} found)")
    for a in news[:25]:
        st.markdown(
            f"""
<div class="card">
  <div class="meta">
    <span class="source">{a['source']}</span>
    <span>{time_ago(a.get('_ts', 0.0))} ago</span>
    <span class="badge">kw={a.get('_kw_hits', 0)}</span>
    <span class="badge">noise={a.get('_noise_hits', 0)}</span>
    <span style="margin-left:10px;">| {a.get('time','')}</span>
  </div>
  <div class="title">
    <a href="{a['link']}" target="_blank" style="color:#e6edf3; text-decoration:none;">
      {a['title']}
    </a>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )



# =========================
# SETTINGS & CONTROLS (AT THE BOTTOM)
# =========================
st.markdown("---")
combined_input = st.text_input(
    "Enter keywords (comma-separated)",
    value=", ".join(st.session_state["auto_keywords"]),
    key="combined_keywords_input"
)
manual_keywords = [k.strip() for k in combined_input.split(",") if k.strip()]

st.markdown("#### ⚡ Filter Settings")
colC, colD = st.columns(2)

with colC:
    min_kw_hits = st.slider("Min KW", 1, 5, 1, key="min_kw_slider")

with colD:
    max_noise_hits = st.slider("Noise", 0, 3, 0, key="max_noise_slider")


# =========================
# AUTO FETCH (every 30s)
# =========================
now_ts = time.time()
if (now_ts - st.session_state["last_fetch_ts"]) >= AUTO_REFRESH_SECONDS:
    with st.spinner("Auto-fetching latest news..."):
        items = []
        
        # Use only manual keywords (source of truth from input)
        combined_keywords = manual_keywords

        try:
            items.extend(fetch_google_news(combined_keywords))
        except Exception as e:
            st.warning(f"GoogleNews fetch error: {e}")

        try:
            items.extend(fetch_bing_news(combined_keywords))
        except Exception as e:
            st.warning(f"BingNews fetch error: {e}")

        items = dedupe(items)
        items = filter_institutional(items, min_kw=min_kw_hits, max_noise=max_noise_hits)
        items = sort_most_recent(items)

        st.session_state["latest_news"] = items
        st.session_state["last_fetch_ts"] = now_ts

st.markdown("---")
st.markdown("*Developed by Ozy | © 2025 | Institutional News Scanner |*")
