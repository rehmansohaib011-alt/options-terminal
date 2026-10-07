import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import html

# ============================================================
# PAGE CONFIG + CSS
# ============================================================
st.set_page_config(
    page_title="T.W.S GAMMA TERMINAL",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

/* ===== BASE ===== */
html, body, .stApp {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  overflow-x: hidden !important;
  max-width: 100vw;
}
.stApp {
  background:
    radial-gradient(ellipse 80% 50% at 10% -10%, rgba(44,109,255,.12) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 90% 0%, rgba(184,65,255,.08) 0%, transparent 45%),
    linear-gradient(160deg, #050711 0%, #090d1b 45%, #050711 100%);
  color: #f3f6ff;
}
.block-container {
  max-width: 1480px !important;
  padding-top: 1rem !important;
  padding-bottom: 2.5rem !important;
  padding-left: 1.25rem !important;
  padding-right: 1.25rem !important;
  position: relative;
  z-index: 1;
  box-sizing: border-box;
}
.block-container, .block-container * {
  box-sizing: border-box;
}

/* ===== TOP COMMAND BAR ===== */
.tws-command {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 12px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(13,20,38,.95), rgba(7,11,22,.97));
  border: 1px solid #26385d;
  box-shadow: 0 8px 28px rgba(0,0,0,.25);
  overflow: hidden;
  min-width: 0;
}
.tws-command:before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,.05) 50%, transparent 70%);
  transform: translateX(-120%);
  animation: twsSweep 9s ease-in-out infinite;
  pointer-events: none;
  will-change: transform;
}
@keyframes twsSweep {
  0%, 65% { transform: translateX(-120%); }
  85%, 100% { transform: translateX(120%); }
}
.tws-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1 1 auto;
  overflow: hidden;
}
.tws-mark {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-weight: 900;
  font-size: 14px;
  color: #fff;
  background: linear-gradient(145deg, #6d5cff, #2e7bff);
  box-shadow: 0 0 18px rgba(75,100,255,.3);
  transition: transform .3s ease, box-shadow .3s ease;
}
.tws-mark:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 24px rgba(75,100,255,.45);
}
.tws-title {
  font-size: 14px;
  font-weight: 900;
  letter-spacing: .6px;
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tws-caption {
  font-size: 9px;
  color: #71819e;
  margin-top: 2px;
  letter-spacing: .8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tws-current {
  color: #9aa8c0;
  font-size: 11px;
  flex-shrink: 0;
  white-space: nowrap;
}
.tws-current b { color: #fff; }

/* Search / popover button – clean circular icon, no hang */
div[data-testid="stPopover"] > button {
  width: 42px !important;
  height: 42px !important;
  min-height: 42px !important;
  padding: 0 !important;
  border-radius: 12px !important;
  background: linear-gradient(145deg, rgba(65,104,255,.25), rgba(114,85,255,.2)) !important;
  border: 1px solid #3a4f8a !important;
  color: #c5d0ff !important;
  font-size: 18px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  transition: transform .25s cubic-bezier(.16,1,.3,1), box-shadow .25s ease, border-color .25s ease !important;
  box-shadow: 0 4px 14px rgba(0,0,0,.2) !important;
}
div[data-testid="stPopover"] > button:hover {
  transform: translateY(-2px) scale(1.04) !important;
  border-color: #5b7dff !important;
  box-shadow: 0 8px 22px rgba(65,104,255,.28) !important;
  background: linear-gradient(145deg, rgba(65,104,255,.4), rgba(114,85,255,.35)) !important;
}
div[data-testid="stPopover"] > button:active {
  transform: scale(.96) !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070b17, #0b1020) !important;
  border-right: 1px solid #202d50;
}
section[data-testid="stSidebar"] > div {
  background: transparent !important;
}

/* ===== HERO ===== */
.hero {
  position: relative;
  overflow: hidden;
  padding: 22px 26px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(22,34,76,.96), rgba(10,14,30,.95));
  border: 1px solid #2c3d70;
  box-shadow: 0 0 30px rgba(66,103,255,.12);
  margin-bottom: 16px;
  transition: border-color .35s ease, box-shadow .35s ease;
}
.hero:hover {
  border-color: #40599a;
  box-shadow: 0 12px 40px rgba(55,88,255,.14);
}
.hero-title {
  font-size: clamp(22px, 4vw, 32px);
  font-weight: 800;
  letter-spacing: -0.8px;
  line-height: 1.15;
  word-break: break-word;
}
.hero-sub {
  color: #8f9dbc;
  margin-top: 6px;
  font-size: clamp(11px, 1.8vw, 14px);
  line-height: 1.45;
}
.live-badge {
  display: inline-block;
  padding: 4px 11px;
  border-radius: 999px;
  color: #51f2b1;
  background: rgba(25,92,69,.22);
  border: 1px solid #24785d;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: .7px;
  margin-bottom: 8px;
  animation: vipLive 2.8s ease-in-out infinite;
}
@keyframes vipLive {
  0%, 100% { box-shadow: 0 0 0 0 rgba(81,242,177,0); }
  50% { box-shadow: 0 0 16px 0 rgba(81,242,177,.18); }
}

/* ===== METRIC + LEVEL CARDS ===== */
.metric-card, .level-card {
  position: relative;
  overflow: hidden;
  border-radius: 14px;
  transition: transform .3s cubic-bezier(.16,1,.3,1), border-color .3s ease, box-shadow .3s ease;
  will-change: transform;
}
.metric-card {
  min-height: 108px;
  padding: 16px;
  background: linear-gradient(145deg, rgba(23,34,65,.94), rgba(9,14,28,.96));
  border: 1px solid #26365f;
  box-shadow: 0 8px 24px rgba(0,0,0,.22);
}
.level-card {
  padding: 16px;
  background: rgba(13,19,38,.9);
  border: 1px solid #233256;
}
.metric-card:hover, .level-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 32px rgba(0,0,0,.3);
}
.metric-card:hover { border-color: #536fd0; }
.metric-label {
  color: #7f8eaf;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .9px;
  text-transform: uppercase;
}
.metric-value {
  color: #f8faff;
  font-size: clamp(18px, 2.4vw, 24px);
  font-weight: 800;
  margin-top: 6px;
  line-height: 1.2;
  word-break: break-word;
}
.metric-sub {
  color: #637292;
  font-size: 10px;
  margin-top: 4px;
}
.level-name {
  font-size: 10px;
  color: #7e8cac;
  text-transform: uppercase;
  letter-spacing: .9px;
}
.level-price {
  font-size: clamp(18px, 2.5vw, 22px);
  font-weight: 800;
  margin-top: 5px;
  line-height: 1.2;
}
.pos { color: #3ddc97; }
.neg { color: #ff5d73; }

/* Level colour variants */
.level-card.level-call {
  border-color: rgba(61,220,151,.35);
  background: linear-gradient(145deg, rgba(13,58,48,.5), rgba(9,14,28,.96));
}
.level-card.level-call .level-price { color: #3ddc97; }
.level-card.level-put {
  border-color: rgba(255,93,115,.35);
  background: linear-gradient(145deg, rgba(67,22,36,.48), rgba(9,14,28,.96));
}
.level-card.level-put .level-price { color: #ff5d73; }
.level-card.level-flip {
  border-color: rgba(255,209,102,.35);
  background: linear-gradient(145deg, rgba(74,58,20,.42), rgba(9,14,28,.96));
}
.level-card.level-flip .level-price { color: #ffd166; }
.level-card.level-pain {
  border-color: rgba(120,137,255,.35);
  background: linear-gradient(145deg, rgba(31,35,78,.48), rgba(9,14,28,.96));
}
.level-card.level-pain .level-price { color: #9aa7ff; }

/* ===== SECTION TITLES ===== */
.section-title {
  font-size: clamp(15px, 2.2vw, 17px);
  font-weight: 800;
  margin: 22px 0 10px;
  color: #e5eaff;
}

/* ===== BUTTONS ===== */
.stButton > button {
  width: 100%;
  height: 44px;
  border: none !important;
  border-radius: 11px !important;
  background: linear-gradient(90deg, #4168ff, #7255ff) !important;
  color: white !important;
  font-weight: 800 !important;
  transition: transform .25s cubic-bezier(.16,1,.3,1), box-shadow .25s ease, filter .25s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(65,104,255,.3) !important;
  filter: brightness(1.08);
}
.stButton > button:active {
  transform: scale(.98);
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
  border: 1px solid #243354;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 28px rgba(0,0,0,.18);
}

/* ===== FOOTER + HIDE STREAMLIT CHROME ===== */
.footer {
  text-align: center;
  color: #52617e;
  font-size: 11px;
  padding-top: 28px;
}
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }
header[data-testid="stHeader"] { height: 0 !important; }

/* ===== RESPONSIVE – DESKTOP ===== */
@media (min-width: 1100px) {
  .block-container {
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }
  .hero { min-height: 140px; display: flex; flex-direction: column; justify-content: center; }
  .metric-card { min-height: 118px; }
  .level-card { min-height: 100px; }
}

/* ===== RESPONSIVE – TABLET ===== */
@media (max-width: 1099px) {
  .metric-card { min-height: 100px; padding: 14px; }
  .metric-value { font-size: 20px; }
  .level-price { font-size: 20px; }
}

/* ===== RESPONSIVE – MOBILE ===== */
@media (max-width: 700px) {
  .block-container {
    padding: 8px 10px 28px !important;
  }
  .tws-command {
    padding: 10px 12px;
    margin-bottom: 10px;
    border-radius: 12px;
    gap: 8px;
  }
  .tws-mark { width: 28px; height: 28px; border-radius: 8px; font-size: 12px; }
  .tws-title { font-size: 12px; }
  .tws-caption { font-size: 8px; }
  .tws-current { font-size: 10px; }
  div[data-testid="stPopover"] > button {
    width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    border-radius: 10px !important;
    font-size: 16px !important;
  }
  .hero {
    padding: 16px 14px;
    border-radius: 14px;
    margin-bottom: 12px;
  }
  .hero-title { font-size: 20px; }
  .hero-sub { font-size: 11px; }
  .live-badge { font-size: 9px; padding: 3px 8px; }
  .metric-card {
    min-height: 88px;
    padding: 12px;
    border-radius: 12px;
  }
  .metric-label { font-size: 9px; }
  .metric-value { font-size: 18px; margin-top: 4px; }
  .metric-sub { font-size: 9px; }
  .level-card {
    padding: 12px;
    border-radius: 12px;
    min-height: 84px;
  }
  .level-price { font-size: 18px; }
  .section-title { font-size: 14px; margin: 16px 0 8px; }
  [data-testid="stDataFrame"] { font-size: 11px; }
  .stButton > button { height: 42px; }
}

/* ===== VERY SMALL PHONES ===== */
@media (max-width: 400px) {
  .tws-title { font-size: 11px; }
  .tws-current { font-size: 9px; }
  .hero-title { font-size: 18px; }
  .metric-card { padding: 10px; min-height: 80px; }
  .metric-value { font-size: 16px; }
  .level-card { padding: 10px; }
  .level-price { font-size: 16px; }
}

/* ===== REDUCED MOTION ===== */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ===== NEWS INTELLIGENCE ===== */
.news-panel{margin:8px 0 18px;padding:16px;border:1px solid #29385f;border-radius:16px;background:linear-gradient(145deg,rgba(16,25,50,.96),rgba(7,11,23,.98));box-shadow:0 10px 30px rgba(0,0,0,.24)}
.news-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}.news-title{font-size:16px;font-weight:900;letter-spacing:.4px}.news-sub{font-size:10px;color:#71819e;margin-top:3px}.news-badge{font-size:9px;font-weight:900;color:#51f2b1;border:1px solid #24785d;background:rgba(25,92,69,.2);padding:5px 9px;border-radius:999px}.news-item{padding:12px 0;border-top:1px solid #1d2945}.news-item:first-child{border-top:0}.news-meta{display:flex;align-items:center;gap:7px;font-size:9px;color:#6f7e9b;margin-bottom:5px}.news-impact{padding:3px 7px;border-radius:999px;font-weight:900}.news-high{color:#ff667d;background:rgba(255,93,115,.12);border:1px solid rgba(255,93,115,.3)}.news-med{color:#ffd166;background:rgba(255,209,102,.1);border:1px solid rgba(255,209,102,.25)}.news-normal{color:#91a2c4;background:rgba(145,162,196,.08);border:1px solid rgba(145,162,196,.18)}.news-link{color:#eaf0ff!important;text-decoration:none!important;font-size:12px;font-weight:700;line-height:1.4}.news-link:hover{color:#7fa0ff!important}.news-empty{color:#72819d;font-size:11px;padding:10px 0}

</style>
""", unsafe_allow_html=True)

TICKERS = ["SPY", "QQQ", "IWM", "NVDA", "AMD", "AAPL", "TSLA", "MSFT", "META", "AMZN",
           "GOOGL", "NFLX", "AVGO", "INTC", "MU", "PLTR", "SMCI", "SMH", "SOXL", "COIN"]

# ============================================================
# SIDEBAR
# ============================================================
if "tws_ticker" not in st.session_state:
    st.session_state.tws_ticker = "SPY"

def normalize_symbol(value: str) -> str:
    value = value.strip().upper().replace(" ", "")
    crypto = {"BTC":"BTC-USD","BITCOIN":"BTC-USD","ETH":"ETH-USD","ETHEREUM":"ETH-USD","SOL":"SOL-USD","SOLANA":"SOL-USD","DOGE":"DOGE-USD","DOGECOIN":"DOGE-USD","XRP":"XRP-USD","BNB":"BNB-USD"}
    return crypto.get(value, value)

# Compact command bar stays visible on desktop and mobile.
bar_left, bar_right = st.columns([10, 1.2], vertical_alignment="center")
with bar_left:
    st.markdown(f"""
    <div class="tws-command">
      <div class="tws-brand"><div class="tws-mark">T</div><div><div class="tws-title">T.W.S GAMMA TERMINAL</div><div class="tws-caption">OPTIONS MARKET INTELLIGENCE</div></div></div>
      <div class="tws-current">SELECTED&nbsp; <b>{st.session_state.tws_ticker}</b></div>
    </div>
    """, unsafe_allow_html=True)

# Top search icon: usable on phone and desktop without opening the sidebar.
with bar_right:
    with st.popover("🔍", help="Search symbol"):
        st.markdown("### Select Market")
        search_value = st.text_input("Stock / Crypto / ETF symbol", value=st.session_state.tws_ticker, placeholder="AAPL, NVDA, SPY, BTC, ETH…", key="tws_symbol_input")
        quick_list = ["SPY","QQQ","NVDA","AAPL","TSLA","MSFT","BTC-USD","ETH-USD"]
        current = st.session_state.tws_ticker if st.session_state.tws_ticker in quick_list else "SPY"
        quick = st.selectbox("Quick select", quick_list, index=quick_list.index(current))
        c1,c2=st.columns(2)
        if c1.button("✓ Apply", use_container_width=True):
            st.session_state.tws_ticker = normalize_symbol(search_value)
            st.cache_data.clear()
            st.rerun()
        if c2.button("⚡ Quick", use_container_width=True):
            st.session_state.tws_ticker = normalize_symbol(quick)
            st.cache_data.clear()
            st.rerun()

with st.sidebar:
    st.markdown("## ⚡ TERMINAL CONTROLS")
    n_exp = st.slider("Expirations to load", 1, 12, 6)
    window = st.slider("Strike window around spot (±%)", 5, 40, 15)
    st.markdown("---")
    if st.button("🚀 ANALYZE / REFRESH"):
        st.cache_data.clear()
        st.rerun()
    st.caption("Data: Yahoo Finance (yfinance), ~15 min delayed. GEX = estimate from public open interest, assuming dealers are long calls / short puts.")

ticker = st.session_state.tws_ticker


# ============================================================
# NEWS INTELLIGENCE
# ============================================================
HIGH_IMPACT_WORDS=["fed","fomc","interest rate","rate decision","cpi","inflation","ppi","nfp","nonfarm","jobs report","payroll","gdp","powell","sec","regulation","approval","etf","lawsuit","ban","hack","earnings","guidance","revenue","forecast","downgrade","upgrade","acquisition","merger","bankruptcy","default","tariff","sanctions"]
MEDIUM_IMPACT_WORDS=["launch","partnership","product","analyst","outlook","production","supply","demand","investor","funding","buyback","dividend"]

def _news_impact(title):
    t=(title or "").lower()
    if any(k in t for k in HIGH_IMPACT_WORDS): return "HIGH","news-high"
    if any(k in t for k in MEDIUM_IMPACT_WORDS): return "MEDIUM","news-med"
    return "NORMAL","news-normal"

@st.cache_data(ttl=300, show_spinner=False)
def _read_rss(url, source_fallback="Market News"):
    """Read an RSS feed without requiring an extra pip package."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; TWS-Gamma-Terminal/1.0)"})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read()
        root = ET.fromstring(raw)
    except Exception:
        return []

    rows = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        source = (item.findtext("source") or source_fallback).strip()
        if not title or not link:
            continue
        try:
            ts = pd.Timestamp(pub).timestamp() if pub else time.time()
        except Exception:
            ts = time.time()
        rows.append({"title": title, "publisher": source or source_fallback, "link": link, "ts": float(ts)})
    return rows


@st.cache_data(ttl=300, show_spinner=False)
def load_symbol_news(symbol):
    """Symbol news: Yahoo Finance RSS -> Google News RSS -> yfinance fallback."""
    symbol = str(symbol).strip().upper()
    now = time.time()
    candidates = []

    # Primary: Yahoo Finance's per-symbol RSS feed.
    yahoo_url = (
        "https://feeds.finance.yahoo.com/rss/2.0/headline?"
        + urllib.parse.urlencode({"s": symbol, "region": "US", "lang": "en-US"})
    )
    candidates.extend(_read_rss(yahoo_url, "Yahoo Finance"))

    # Backup: Google News RSS search for the selected symbol.
    if len(candidates) < 3:
        q = urllib.parse.quote(f'"{symbol}" stock when:24h')
        google_url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
        candidates.extend(_read_rss(google_url, "Google News"))

    # Final fallback: yfinance's news endpoint.
    if len(candidates) < 3:
        try:
            items = yf.Ticker(symbol).news or []
            for item in items:
                content = item.get("content", item) if isinstance(item, dict) else {}
                title = content.get("title") or item.get("title")
                if not title:
                    continue
                ts = content.get("providerPublishTime") or item.get("providerPublishTime")
                if not ts:
                    pub = content.get("pubDate") or item.get("pubDate")
                    try:
                        ts = pd.Timestamp(pub).timestamp() if pub else now
                    except Exception:
                        ts = now
                provider = content.get("provider", {})
                publisher = provider.get("displayName") if isinstance(provider, dict) else None
                publisher = publisher or item.get("publisher") or "Market News"
                cu = content.get("canonicalUrl")
                ct = content.get("clickThroughUrl")
                link = cu.get("url") if isinstance(cu, dict) else None
                link = link or (ct.get("url") if isinstance(ct, dict) else None)
                link = link or item.get("link") or "#"
                candidates.append({"title": title, "publisher": publisher, "link": link, "ts": float(ts)})
        except Exception:
            pass

    # Deduplicate and keep only the latest 24 hours.
    seen = set()
    out = []
    for item in candidates:
        title = str(item.get("title") or "").strip()
        link = str(item.get("link") or "").strip()
        if not title or not link:
            continue
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        try:
            age = max(0.0, (now - float(item.get("ts", now))) / 3600.0)
        except Exception:
            age = 0.0
        if age > 24:
            continue
        impact, cls = _news_impact(title)
        out.append({"title": title, "publisher": str(item.get("publisher") or "Market News"), "link": link, "age": age, "impact": impact, "cls": cls})

    out.sort(key=lambda x: (0 if x["impact"] == "HIGH" else 1 if x["impact"] == "MEDIUM" else 2, x["age"]))
    return out[:8]

news_items = load_symbol_news(ticker)
st.markdown(
    f"""<div class="news-panel"><div class="news-head"><div><div class="news-title">📰 MAJOR NEWS · {html.escape(ticker)}</div><div class="news-sub">Symbol-linked market headlines · Last 24 hours · RSS + Yahoo fallback</div></div><div class="news-badge">● LIVE FEED</div></div>""",
    unsafe_allow_html=True,
)
if news_items:
    for n in news_items:
        age_txt = f"{n['age']:.1f}h ago" if n['age'] >= 1 else f"{max(1, int(n['age'] * 60))}m ago"
        safe_title = html.escape(str(n['title']))
        safe_pub = html.escape(str(n['publisher']))
        safe_link = html.escape(str(n['link']), quote=True)
        st.markdown(
            f"""<div class="news-item"><div class="news-meta"><span class="news-impact {n['cls']}">{n['impact']}</span><span>{safe_pub}</span><span>·</span><span>{age_txt}</span></div><a class="news-link" href="{safe_link}" target="_blank" rel="noopener noreferrer">{safe_title}</a></div>""",
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        '<div class="news-empty">No symbol-specific headlines were returned in the last 24 hours. Try ANALYZE / REFRESH or select another symbol.</div>',
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
  <div class="live-badge">● LIVE OPTIONS DATA</div>
  <div class="hero-title">T.W.S GAMMA TERMINAL</div>
  <div class="hero-sub">OPTIONS MARKET INTELLIGENCE · Call Wall · Put Wall · Gamma Flip · Max Pain · IV · GEX</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MATH (vectorized)
# ============================================================
def bs_gamma(S, K, T, sigma, r=0.0):
    S = np.asarray(S, dtype=float)
    with np.errstate(all="ignore"):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        g = np.exp(-0.5 * d1 ** 2) / np.sqrt(2 * np.pi) / (S * sigma * np.sqrt(T))
    return np.nan_to_num(g, nan=0.0, posinf=0.0, neginf=0.0)


def total_gex_at(S, K, T, iv, oi, sign):
    """Net dollar gamma per 1% move at hypothetical spot S."""
    g = bs_gamma(S, K, T, iv)
    return float(np.sum(g * oi * 100 * S * S * 0.01 * sign))


def max_pain(chain):
    calls = chain[chain["side"] == "CALL"]
    puts = chain[chain["side"] == "PUT"]
    strikes = np.sort(chain["strike"].dropna().unique())
    if len(strikes) == 0 or chain["openInterest"].sum() == 0:
        return np.nan
    ck, co = calls["strike"].values, calls["openInterest"].values
    pk, po = puts["strike"].values, puts["openInterest"].values
    pain = [np.sum(np.maximum(p - ck, 0) * co) + np.sum(np.maximum(pk - p, 0) * po) for p in strikes]
    return float(strikes[int(np.argmin(pain))])


# ============================================================
# DATA
# ============================================================
import re
import requests


def _clean(df):
    df["openInterest"] = pd.to_numeric(df["openInterest"], errors="coerce").fillna(0.0)
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0.0)
    df["impliedVolatility"] = pd.to_numeric(df["impliedVolatility"], errors="coerce").fillna(0.0)
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    return df.dropna(subset=["strike"])


def load_yahoo(symbol, n_exp):
    stock = yf.Ticker(symbol)
    spot = None
    try:
        spot = float(stock.fast_info["lastPrice"])
    except Exception:
        pass
    if not spot or np.isnan(spot):
        hist = stock.history(period="5d")
        if hist.empty:
            raise ValueError("Yahoo: no price")
        spot = float(hist["Close"].iloc[-1])

    expirations = list(stock.options)
    if not expirations:
        raise ValueError("Yahoo: no options")

    rows = []
    for exp in expirations[:n_exp]:
        try:
            oc = stock.option_chain(exp)
        except Exception:
            continue
        c, p = oc.calls.copy(), oc.puts.copy()
        c["side"], p["side"] = "CALL", "PUT"
        for d in (c, p):
            d["expiration"] = exp
        rows += [c, p]
    if not rows:
        raise ValueError("Yahoo: chain empty")
    return spot, _clean(pd.concat(rows, ignore_index=True))


def load_cboe(symbol, n_exp):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = None
    for sym in (symbol, "_" + symbol):  # indices use underscore prefix
        url = f"https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json"
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                data = r.json().get("data")
                if data and data.get("options"):
                    break
        except Exception:
            continue
    if not data or not data.get("options"):
        raise ValueError("Cboe: no data")

    spot = data.get("current_price") or data.get("close") or data.get("prev_day_close")
    spot = float(spot)

    pat = re.compile(r"^(.*?)(\d{6})([CP])(\d{8})$")
    rows = []
    for o in data["options"]:
        m = pat.match(str(o.get("option", "")))
        if not m:
            continue
        _, yymmdd, cp, strike = m.groups()
        rows.append({
            "strike": int(strike) / 1000.0,
            "side": "CALL" if cp == "C" else "PUT",
            "expiration": datetime.strptime(yymmdd, "%y%m%d").strftime("%Y-%m-%d"),
            "openInterest": o.get("open_interest"),
            "volume": o.get("volume"),
            "impliedVolatility": o.get("iv"),
        })
    if not rows:
        raise ValueError("Cboe: parse failed")
    df = pd.DataFrame(rows)
    today = pd.Timestamp.today().normalize()
    df = df[pd.to_datetime(df["expiration"]) >= today]
    keep = sorted(df["expiration"].unique())[:n_exp]
    df = df[df["expiration"].isin(keep)]
    return spot, _clean(df.reset_index(drop=True))


@st.cache_data(ttl=120, show_spinner="Fetching live option chain...")
def load_options(symbol, n_exp):
    errors = []
    for attempt in range(2):
        try:
            spot, df = load_yahoo(symbol, n_exp)
            return spot, df, "Yahoo Finance"
        except Exception as e:
            errors.append(str(e))
            time.sleep(1)
    try:
        spot, df = load_cboe(symbol, n_exp)
        return spot, df, "Cboe (delayed)"
    except Exception as e:
        errors.append(str(e))
    raise ValueError(f"No options data for {symbol}. Tried: " + " | ".join(dict.fromkeys(errors)))


# ============================================================
# ANALYSIS
# ============================================================
try:
    spot, opt, source = load_options(ticker, n_exp)
except Exception as e:
    st.error(f"❌ {e}")
    st.stop()

# time to expiry (expiry at 4pm ET close ≈ end of that day)
exp_ts = pd.to_datetime(opt["expiration"]) + pd.Timedelta(hours=20)
days = (exp_ts - pd.Timestamp.utcnow().tz_localize(None)).dt.total_seconds() / 86400
opt["T"] = np.maximum(days.values, 0.5) / 365.0
opt["sign"] = np.where(opt["side"] == "CALL", 1.0, -1.0)

# usable rows for gamma (valid IV + OI)
valid = (opt["impliedVolatility"] > 0.01) & (opt["impliedVolatility"] < 5) & (opt["openInterest"] > 0)
g_opt = opt[valid].copy()

K = g_opt["strike"].values.astype(float)
T = g_opt["T"].values
IV = g_opt["impliedVolatility"].values
OI = g_opt["openInterest"].values
SG = g_opt["sign"].values

g_opt["GEX"] = bs_gamma(spot, K, T, IV) * OI * 100 * spot * spot * 0.01 * SG
net_gex = float(g_opt["GEX"].sum())

# walls: calls above spot, puts below spot (fallback: overall)
calls = opt[opt["side"] == "CALL"]
puts = opt[opt["side"] == "PUT"]
c_oi = calls.groupby("strike")["openInterest"].sum()
p_oi = puts.groupby("strike")["openInterest"].sum()
c_above = c_oi[c_oi.index >= spot]
p_below = p_oi[p_oi.index <= spot]
call_wall = float((c_above if not c_above.empty else c_oi).idxmax())
put_wall = float((p_below if not p_below.empty else p_oi).idxmax())

# gamma flip: where total GEX profile crosses zero (recomputed across spot prices)
grid = np.linspace(spot * 0.8, spot * 1.2, 161)
profile = np.array([total_gex_at(s, K, T, IV, OI, SG) for s in grid])
gamma_flip = np.nan
cross = np.where(np.sign(profile[:-1]) * np.sign(profile[1:]) < 0)[0]
if len(cross):
    best = min(cross, key=lambda i: abs(grid[i] - spot))
    x0, x1, y0, y1 = grid[best], grid[best + 1], profile[best], profile[best + 1]
    gamma_flip = float(x0 - y0 * (x1 - x0) / (y1 - y0))

# max pain on nearest expiration with OI, plus per-expiration table
mp_rows = []
for exp, ch in opt.groupby("expiration", sort=True):
    ch_t = ch["T"].iloc[0]
    near = ch.iloc[(ch["strike"] - spot).abs().argsort()[:6]]
    atm_iv = near.loc[near["impliedVolatility"] > 0.01, "impliedVolatility"].mean() * 100
    pc = ch.loc[ch.side == "PUT", "openInterest"].sum() / max(ch.loc[ch.side == "CALL", "openInterest"].sum(), 1)
    mp_rows.append({
        "Expiration": exp,
        "DTE": round(ch_t * 365, 1),
        "Max Pain": max_pain(ch),
        "ATM IV %": round(atm_iv, 2) if pd.notna(atm_iv) else np.nan,
        "Put/Call OI": round(pc, 2),
        "Total OI": int(ch["openInterest"].sum()),
        "Volume": int(ch["volume"].sum()),
    })
exp_table = pd.DataFrame(mp_rows)
valid_mp = exp_table.dropna(subset=["Max Pain"])
mp_main = float(valid_mp["Max Pain"].iloc[0]) if not valid_mp.empty else np.nan
atm_main = exp_table["ATM IV %"].dropna()
atm_iv = float(atm_main.iloc[0]) if not atm_main.empty else np.nan

levels = [x for x in [call_wall, put_wall, gamma_flip, mp_main] if pd.notna(x)]
magnetic = min(levels, key=lambda x: abs(x - spot)) if levels else np.nan

# ============================================================
# HEADER + METRICS
# ============================================================
st.markdown(f"### {ticker} &nbsp; <span style='color:#7383a5;font-size:14px'>Spot "
            f"<b style='color:#fff'>${spot:,.2f}</b> · Source: {source} · {datetime.now():%H:%M:%S}</span>",
            unsafe_allow_html=True)


def fmt(x):
    return f"${x:,.2f}" if pd.notna(x) else "N/A"


metrics = [
    ("SPOT PRICE", fmt(spot), "Underlying"),
    ("CALL WALL", fmt(call_wall), "Highest call OI above spot"),
    ("PUT WALL", fmt(put_wall), "Highest put OI below spot"),
    ("GAMMA FLIP", fmt(gamma_flip), "Total GEX crosses zero"),
    ("MAX PAIN", fmt(mp_main), f"Nearest exp ({valid_mp['Expiration'].iloc[0]})" if not valid_mp.empty else ""),
    ("ATM IV", f"{atm_iv:.2f}%" if pd.notna(atm_iv) else "N/A", "Nearest expiration"),
]
for col, (label, value, sub) in zip(st.columns(6), metrics):
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

# ============================================================
# KEY LEVELS
# ============================================================
st.markdown('<div class="section-title">🎯 Key Market Structure</div>', unsafe_allow_html=True)
call_dist = (call_wall / spot - 1) * 100
put_dist = (put_wall / spot - 1) * 100
regime = "Positive Gamma (dampening)" if net_gex > 0 else "Negative Gamma (amplifying)"
cls = "pos" if net_gex > 0 else "neg"

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="level-card level-pain"><div class="level-name">Magnetic Level</div>'
            f'<div class="level-price">{fmt(magnetic)}</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="level-card level-call"><div class="level-name">Call Wall Distance</div>'
            f'<div class="level-price">{call_dist:+.2f}%</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="level-card level-put"><div class="level-name">Put Wall Distance</div>'
            f'<div class="level-price">{put_dist:+.2f}%</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="level-card level-flip"><div class="level-name">Net GEX / 1% move</div>'
            f'<div class="level-price {cls}">${net_gex / 1e9:,.2f}B</div>'
            f'<div class="metric-sub">{regime}</div></div>', unsafe_allow_html=True)

# ============================================================
# CHARTS
# ============================================================
lo, hi = spot * (1 - window / 100), spot * (1 + window / 100)
chart_cfg = dict(height=340)


def rule(x, color, label):
    if pd.isna(x):
        return alt.Chart(pd.DataFrame({"x": [], "l": []})).mark_rule()
    d = pd.DataFrame({"x": [x], "l": [label]})
    r = alt.Chart(d).mark_rule(color=color, strokeDash=[5, 4], size=2).encode(x="x:Q")
    t = alt.Chart(d).mark_text(color=color, align="left", dx=4, dy=-8, fontSize=11, y=0).encode(x="x:Q", text="l:N")
    return r + t


st.markdown('<div class="section-title">📊 Net GEX by Strike</div>', unsafe_allow_html=True)
gs = (g_opt.groupby("strike")["GEX"].sum().reset_index())
gs = gs[(gs.strike >= lo) & (gs.strike <= hi)]
gs["GEX_M"] = gs["GEX"] / 1e6
gs["dir"] = np.where(gs["GEX_M"] >= 0, "Positive", "Negative")
bars = alt.Chart(gs).mark_bar().encode(
    x=alt.X("strike:Q", title="Strike", scale=alt.Scale(domain=[lo, hi])),
    y=alt.Y("GEX_M:Q", title="GEX ($M per 1%)"),
    color=alt.Color("dir:N", scale=alt.Scale(domain=["Positive", "Negative"], range=["#31e6a2", "#ff4d6d"]), legend=None),
    tooltip=["strike", alt.Tooltip("GEX_M:Q", format=",.1f")],
)
st.altair_chart((bars + rule(spot, "#ffffff", "Spot") + rule(gamma_flip, "#ffd166", "Flip")
                 + rule(call_wall, "#3ddc97", "Call Wall") + rule(put_wall, "#ff5d73", "Put Wall")
                 ).properties(**chart_cfg), use_container_width=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="section-title">🧱 Open Interest by Strike</div>', unsafe_allow_html=True)
    oi_df = opt.groupby(["strike", "side"])["openInterest"].sum().reset_index()
    oi_df = oi_df[(oi_df.strike >= lo) & (oi_df.strike <= hi)]
    oi_chart = alt.Chart(oi_df).mark_bar(opacity=.9).encode(
        x=alt.X("strike:Q", title="Strike", scale=alt.Scale(domain=[lo, hi])),
        y=alt.Y("openInterest:Q", title="Open Interest", stack=None),
        color=alt.Color("side:N", scale=alt.Scale(domain=["CALL", "PUT"], range=["#31e6a2", "#ff4d6d"]),
                        legend=alt.Legend(orient="top", title=None)),
        tooltip=["strike", "side", alt.Tooltip("openInterest:Q", format=",")],
    )
    st.altair_chart((oi_chart + rule(spot, "#ffffff", "Spot")).properties(**chart_cfg), use_container_width=True)

with right:
    st.markdown('<div class="section-title">📈 GEX Profile vs Spot Price</div>', unsafe_allow_html=True)
    prof = pd.DataFrame({"price": grid, "GEX_M": profile / 1e6})
    line = alt.Chart(prof).mark_line(color="#7f8cff", size=3).encode(
        x=alt.X("price:Q", title="Hypothetical spot", scale=alt.Scale(zero=False)),
        y=alt.Y("GEX_M:Q", title="Total GEX ($M)"),
    )
    zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#52617e").encode(y="y:Q")
    st.altair_chart((line + zero + rule(spot, "#ffffff", "Spot") + rule(gamma_flip, "#ffd166", "Flip")
                     ).properties(**chart_cfg), use_container_width=True)

# ============================================================
# EXPIRATION TABLE + IV TERM STRUCTURE
# ============================================================
st.markdown('<div class="section-title">📅 Expiration Data</div>', unsafe_allow_html=True)
st.dataframe(exp_table, use_container_width=True, hide_index=True)

iv_plot = exp_table.dropna(subset=["ATM IV %"])
if len(iv_plot) > 1:
    st.markdown('<div class="section-title">🌡️ IV Term Structure</div>', unsafe_allow_html=True)
    ivc = alt.Chart(iv_plot).mark_line(point=True, color="#ffd166", size=3).encode(
        x=alt.X("DTE:Q", title="Days to expiry"),
        y=alt.Y("ATM IV %:Q", scale=alt.Scale(zero=False)),
        tooltip=["Expiration", "DTE", "ATM IV %"],
    )
    st.altair_chart(ivc.properties(height=260), use_container_width=True)

# ============================================================
# TOP STRIKES TABLE
# ============================================================
st.markdown('<div class="section-title">🔝 Top 10 Strikes by Open Interest</div>', unsafe_allow_html=True)
top = (opt.pivot_table(index="strike", columns="side", values="openInterest", aggfunc="sum", fill_value=0)
       .assign(Total=lambda d: d.sum(axis=1)).sort_values("Total", ascending=False).head(10).reset_index())
st.dataframe(top, use_container_width=True, hide_index=True)

st.markdown(
    '<div class="footer">Estimates from delayed public data. GEX assumes dealers are long calls and short puts. '
    'Not financial advice.</div>', unsafe_allow_html=True)
