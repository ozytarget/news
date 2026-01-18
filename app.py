# app.py
# BLOOMBERG MODE — Institutional News Scanner (Google RSS + Bing News)
# Features:
# - Auto refresh every 30s (Streamlit rerun + cached fetch TTL=30s)
# - Hard cutoff: last 24h only (configurable)
# - Bloomberg-like scoring: whitelist/blacklist + clickbait penalties + wire language bonus + high-impact triggers
# - BREAKING TOP 10 + ALL headlines ranked
# - Anti-noise for "options" by excluding sports/travel terms in Google query
#
# Install:
#   pip install streamlit streamlit-autorefresh feedparser requests python-dateutil
#
# Run:
#   streamlit run app.py

import os
import re
import time
from datetime import timezone
from urllib.parse import quote, urlparse

import requests
import streamlit as st
from dateutil import parser as date_parser
from streamlit_autorefresh import st_autorefresh


# =========================
# CONFIG
# =========================
AUTO_REFRESH_SECONDS = 30

# Hard cutoff: only keep articles within last X hours
MAX_ARTICLE_AGE_HOURS = 24

# Good default (you can paste your bigger Bloomberg keyword preset in the UI input)
DEFAULT_KEYWORDS = ["SPY", "FOMC", "Treasury", "yields", "inflation", "options", "gamma", "liquidity"]

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
BING_NEWS_ENDPOINT = "https://api.bing.microsoft.com/v7.0/news/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
}

BING_API_KEY = os.getenv("BING_NEWS_API_KEY", "").strip()


# =========================
# FILTERS (Institutional + Noise)
# =========================
INSTITUTIONAL_KEYWORDS = [
    # FED / CENTRAL BANKS
    "fomc", "fed", "federal reserve", "powell", "minutes", "dot plot",
    "forward guidance", "terminal rate", "rate path", "restrictive", "accommodative",
    "balance sheet", "runoff", "qt", "qe", "ecb", "boj", "boe",

    # MACRO DATA
    "cpi", "ppi", "pce", "core pce", "inflation", "jobs report", "nonfarm payrolls", "nfp",
    "jobless claims", "unemployment", "gdp", "retail sales", "ism", "pmi",

    # TREASURY / RATES
    "treasury", "auction", "bid-to-cover", "bid to cover", "tail",
    "2-year", "2 year", "10-year", "10 year", "real yield", "real yields",
    "yields", "yield curve", "term premium", "curve steepening", "curve flattening",

    # FLOWS / POSITIONING
    "rebalancing", "asset allocation", "positioning", "cta", "risk parity",
    "etf inflows", "etf outflows", "creations", "redemptions",

    # OPTIONS / VOL / DEALER
    "options", "open interest", "gamma", "gamma exposure", "negative gamma", "positive gamma",
    "dealer hedging", "delta hedging", "0dte", "implied volatility", "skew", "vix",

    # LIQUIDITY / SYSTEM
    "liquidity", "funding stress", "financial conditions", "repo", "sofr", "stress",
]

NOISE_KEYWORDS = [
    "meme", "viral", "to the moon", "diamond hands", "paper hands",
    "influencer", "hype", "ape",
    "rockets", "soars", "surges", "plunges",
]


# =========================
# BLOOMBERG SCORING LAYERS
# =========================
SOURCE_WHITELIST = [
    "reuters.com", "bloomberg.com", "ft.com", "wsj.com",
    "federalreserve.gov", "treasury.gov", "bls.gov", "bea.gov",
    "cnbc.com", "marketwatch.com", "barrons.com",
]

SOURCE_BLACKLIST = [
    "prnewswire.com", "businesswire.com", "globenewswire.com",
    "accesswire.com", "newsfilecorp.com",
    "seekingalpha.com", "themotleyfool.com", "investorplace.com",
]

CLICKBAIT_PHRASES = [
    "what you need to know", "explained", "here's why", "here is why",
    "everything you need to know", "you won't believe",
    "price prediction", "forecast", "top picks", "buy now",
]

MODAL_WEAK_WORDS = [
    "could", "might", "may", "likely", "unlikely",
    "expected", "expected to", "set to", "poised to", "seen as",
]

WIRE_PHRASES = [
    "said in a statement", "in a statement",
    "according to people familiar", "people familiar with the matter",
    "sources said", "data showed", "figures showed",
    "markets repriced", "investors reassessed",
    "traders priced in", "priced in",
]

HIGH_IMPACT_TRIGGERS = [
    "cpi", "core cpi", "ppi", "pce", "core pce",
    "nonfarm payrolls", "nfp", "jobless claims", "unemployment rate",
    "fomc", "fed minutes", "dot plot", "powell",
    "auction", "refunding", "bid-to-cover", "tail",
    "2-year", "10-year", "real yield", "sofr", "repo", "qt",
    "vix", "0dte", "gamma", "dealer hedging", "skew",
]

# Anti-noise terms specifically for the word “options”
NEGATIVE_KEYWORDS = [
    # sports
    "quarterback", "broncos", "giants", "nfl", "nba", "mlb", "nhl", "soccer", "football",
    # travel / visas / airlines
    "rebooking", "flight", "flights", "airline", "visa",
    # lifestyle
    "brain", "learning", "health", "fitness",
]


# =========================
# UI
# =========================
st.set_page_config(page_title="Bloomberg Mode News Scanner", layout="wide")

st.markdown(
    """
<style>
.stApp { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); color: #e6edf3; }
.header { color: #79c0ff; font-size: 28px; font-weight: 800; letter-spacing: 1px; font-family: 'Courier New', monospace; }
.card { border-left: 3px solid #1f6feb; padding: 12px 14px; margin-bottom: 10px; background: rgba(20, 20, 30, 0.92); border-radius: 6px; }
.meta { color: #8b949e; font-size: 12px; }
.source { color: #79c0ff; font-size: 12px; font-weight: 700; margin-right: 10px; }
.title { color: #e6edf3; font-size: 15px; font-weight: 650; line-height: 1.35; }
.badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px; margin-left:6px; border:1px solid rgba(121,192,255,.25); color:#79c0ff; }
hr { border: 0; border-top: 1px solid rgba(255,255,255,.08); }
.small { color:#8b949e; font-size:12px; }
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


def filter_institutional(items: list[dict], min_kw: int, max_noise: int) -> list[dict]:
    out = []
    now_ts = time.time()
    max_age_sec = float(MAX_ARTICLE_AGE_HOURS) * 3600.0

    for a in items:
        title = (a.get("title") or "").strip()
        if len(title) < 5:
            continue

        ts = float(a.get("_ts") or 0.0)
        if ts <= 0:
            continue

        # Hard cutoff by time
        if (now_ts - ts) > max_age_sec:
            continue

        blob = f"{title}\n{a.get('summary','')}".strip().lower()

        kw_hits = count_hits(blob, INSTITUTIONAL_KEYWORDS)
        noise_hits = count_hits(blob, NOISE_KEYWORDS)

        if kw_hits >= min_kw and noise_hits <= max_noise:
            b = dict(a)
            b["_kw_hits"] = kw_hits
            b["_noise_hits"] = noise_hits
            out.append(b)

    return out


def _extract_domain(url: str) -> str:
    try:
        host = (urlparse(url).netloc or "").lower()
        return host.replace("www.", "")
    except Exception:
        return ""


def _domain_in(domain: str, patterns: list[str]) -> bool:
    if not domain:
        return False
    return any(p in domain for p in patterns)


def score_bloomberg(item: dict) -> dict:
    title = (item.get("title") or "").strip()
    summary = (item.get("summary") or "").strip()
    blob = f"{title}\n{summary}".lower()

    domain = _extract_domain(item.get("link") or "")
    score = 0
    reasons = []

    kw_hits = int(item.get("_kw_hits", 0))
    noise_hits = int(item.get("_noise_hits", 0))

    # Institutional signal
    if kw_hits:
        add = min(40, kw_hits * 6)
        score += add
        reasons.append(f"+inst({kw_hits})")

    # High impact (macro/rates/options)
    hi_hits = count_hits(blob, HIGH_IMPACT_TRIGGERS)
    if hi_hits:
        add = min(30, hi_hits * 8)
        score += add
        reasons.append(f"+impact({hi_hits})")

    # Wire language
    wire_hits = count_hits(blob, WIRE_PHRASES)
    if wire_hits:
        add = min(16, wire_hits * 8)
        score += add
        reasons.append(f"+wire({wire_hits})")

    # Sources
    if _domain_in(domain, SOURCE_WHITELIST):
        score += 18
        reasons.append("+whitelist")
    if _domain_in(domain, SOURCE_BLACKLIST):
        score -= 28
        reasons.append("-blacklist")

    # Noise penalty
    if noise_hits:
        score -= min(30, noise_hits * 10)
        reasons.append(f"-noise({noise_hits})")

    # Clickbait/modals penalty
    cb_hits = count_hits(blob, CLICKBAIT_PHRASES)
    if cb_hits:
        score -= min(30, cb_hits * 15)
        reasons.append(f"-clickbait({cb_hits})")

    modal_hits = count_hits(blob, MODAL_WEAK_WORDS)
    if modal_hits:
        score -= min(18, modal_hits * 6)
        reasons.append(f"-modal({modal_hits})")

    score = max(-50, min(100, score))

    out = dict(item)
    out["_domain"] = domain
    out["_score"] = score
    out["_reasons"] = " ".join(reasons[:6])
    return out


# =========================
# FETCHERS
# =========================
def fetch_google_news(keywords: list[str]) -> list[dict]:
    base = " OR ".join(keywords) if keywords else "SPY"

    # Force recency on Google News query
    when = (
        "when:1d" if MAX_ARTICLE_AGE_HOURS <= 24
        else "when:2d" if MAX_ARTICLE_AGE_HOURS <= 48
        else "when:7d"
    )

    negative = " ".join([f"-{w}" for w in NEGATIVE_KEYWORDS])

    query = f"({base}) {when} {negative}"
    url = GOOGLE_NEWS_RSS.format(q=quote(query))

    feed = requests.get(url, headers=HEADERS, timeout=12)
    feed.raise_for_status()

    import feedparser
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
    freshness = "Day" if MAX_ARTICLE_AGE_HOURS <= 24 else "Week"

    params = {
        "q": query,
        "mkt": "en-US",
        "count": 25,
        "sortBy": "Date",
        "freshness": freshness,
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
            "summary": "",
            "_ts": ts,
        })
    return items


# =========================
# SMOOTH AUTO-UPDATE (cached fetch)
# =========================
feed_box = st.container()

@st.cache_data(ttl=AUTO_REFRESH_SECONDS, show_spinner=False)
def fetch_all_sources_cached(keywords: list[str], min_kw: int, max_noise: int) -> list[dict]:
    items: list[dict] = []

    try:
        items.extend(fetch_google_news(keywords))
    except Exception:
        pass

    try:
        items.extend(fetch_bing_news(keywords))
    except Exception:
        pass

    items = dedupe(items)
    items = filter_institutional(items, min_kw=min_kw, max_noise=max_noise)
    items = [score_bloomberg(x) for x in items]
    items.sort(key=lambda x: (x.get("_score", 0), x.get("_ts", 0.0)), reverse=True)

    return items


# =========================
# SETTINGS
# =========================
st.markdown("---")
combined_input = st.text_input(
    "Enter keywords (comma-separated)",
    value=", ".join(st.session_state["auto_keywords"]),
    key="combined_keywords_input"
)
manual_keywords = [k.strip() for k in combined_input.split(",") if k.strip()]
st.session_state["auto_keywords"] = manual_keywords

st.markdown("#### ⚡ Filter Settings")
colC, colD = st.columns(2)
with colC:
    min_kw_hits = st.slider("Min KW", 1, 5, 1, key="min_kw_slider")
with colD:
    max_noise_hits = st.slider("Noise", 0, 3, 0, key="max_noise_slider")

colA, colB = st.columns([1, 3])
with colA:
    if st.button("Force Refresh NOW (flush cache)", use_container_width=True, key="force_refresh_flush"):
        fetch_all_sources_cached.clear()
        st.session_state["last_fetch_ts"] = 0.0
with colB:
    st.markdown(
        f"<div class='small'>Auto-refresh every {AUTO_REFRESH_SECONDS}s | Cutoff: last {MAX_ARTICLE_AGE_HOURS}h</div>",
        unsafe_allow_html=True
    )


# =========================
# AUTO FETCH (every 30s)
# =========================
now_ts = time.time()
if (now_ts - st.session_state.get("last_fetch_ts", 0.0)) >= AUTO_REFRESH_SECONDS:
    with st.spinner("Auto-fetching latest news..."):
        st.session_state["latest_news"] = fetch_all_sources_cached(
            keywords=manual_keywords if manual_keywords else DEFAULT_KEYWORDS,
            min_kw=min_kw_hits,
            max_noise=max_noise_hits,
        )
        st.session_state["last_fetch_ts"] = now_ts


# =========================
# RENDER: BREAKING TOP 10 + ALL ranked
# =========================
with feed_box:
    st.markdown('<div class="header">BLOOMBERG MODE — NEWS SCANNER</div>', unsafe_allow_html=True)

    news = st.session_state.get("latest_news") or []

    if not news:
        st.info("📰 Loading news... (first fetch usually takes a few seconds)")
    else:
        breaking = news[:10]
        rest = news[10:60]

        st.subheader("🚨 BREAKING — TOP 10 (ranked by Bloomberg score)")
        for a in breaking:
            st.markdown(
                f"""
<div class="card">
  <div class="meta">
    <span class="source">{a.get('source','')}</span>
    <span>{time_ago(a.get('_ts', 0.0))} ago</span>
    <span class="badge">score={a.get('_score', 0)}</span>
    <span class="badge">kw={a.get('_kw_hits', 0)}</span>
    <span class="badge">noise={a.get('_noise_hits', 0)}</span>
    <span class="badge">{a.get('_domain','')}</span>
    <span style="margin-left:10px;">| {a.get('time','')}</span>
  </div>
  <div class="title">
    <a href="{a.get('link','')}" target="_blank" style="color:#e6edf3; text-decoration:none;">
      {a.get('title','')}
    </a>
    <span class="badge" style="margin-left:8px;">{a.get('_reasons','')}</span>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.subheader(f"📰 ALL HEADLINES (ranked) — showing {len(rest)} of {len(news)}")
        for a in rest:
            st.markdown(
                f"""
<div class="card">
  <div class="meta">
    <span class="source">{a.get('source','')}</span>
    <span>{time_ago(a.get('_ts', 0.0))} ago</span>
    <span class="badge">score={a.get('_score', 0)}</span>
    <span class="badge">{a.get('_domain','')}</span>
    <span style="margin-left:10px;">| {a.get('time','')}</span>
  </div>
  <div class="title">
    <a href="{a.get('link','')}" target="_blank" style="color:#e6edf3; text-decoration:none;">
      {a.get('title','')}
    </a>
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

st.markdown("---")
st.markdown("*Developed by ozy | © 2026 | Bloomberg Mode News Scanner |*")
