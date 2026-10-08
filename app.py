"""
T.W.S TERMINAL — Trade With Sohaib
Professional options + volume + chart terminal.
Run:  streamlit run tws_terminal.py
"""
from __future__ import annotations

import re
import time
from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf

# ═══════════════════════════════════════════════════════════════
# PAGE
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="T.W.S Terminal — Trade With Sohaib",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# CSS — Green cyber theme matching TWS brand
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
  --bg: #05080c;
  --panel: #0b1118;
  --panel2: #101820;
  --border: #1a2a22;
  --border-g: #1e3d2f;
  --green: #00e676;
  --green2: #00c853;
  --green-dim: rgba(0,230,118,.12);
  --green-glow: rgba(0,230,118,.28);
  --red: #ff5252;
  --amber: #ffd740;
  --text: #e8f5e9;
  --muted: #7a8f82;
  --silver: #c0c8d0;
}

html, body, .stApp {
  font-family: 'Inter', system-ui, sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
  overflow-x: hidden !important;
}
.stApp {
  background:
    radial-gradient(ellipse 70% 45% at 15% -5%, rgba(0,230,118,.07) 0%, transparent 55%),
    radial-gradient(ellipse 50% 35% at 90% 0%, rgba(0,200,83,.05) 0%, transparent 50%),
    linear-gradient(165deg, #05080c 0%, #070c10 40%, #05080c 100%) !important;
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden !important; height: 0 !important; }
div[data-testid="stToolbar"] { display: none !important; }
.block-container {
  max-width: 1600px !important;
  padding: 0.6rem 1rem 2rem !important;
}

.tws-top {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 16px; margin-bottom: 10px;
  background: linear-gradient(135deg, rgba(8,16,12,.97), rgba(5,10,8,.98));
  border: 1px solid var(--border-g); border-radius: 14px;
  box-shadow: 0 0 40px rgba(0,230,118,.06), inset 0 1px 0 rgba(0,230,118,.08);
  position: relative; overflow: hidden;
}
.tws-top::before {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(105deg, transparent 40%, rgba(0,230,118,.04) 50%, transparent 60%);
  animation: sheen 8s ease-in-out infinite; pointer-events: none;
}
@keyframes sheen {
  0%, 70% { transform: translateX(-120%); }
  100% { transform: translateX(120%); }
}
.tws-brand-row { display: flex; align-items: center; gap: 12px; min-width: 0; }
.tws-logo-mark {
  width: 42px; height: 42px; border-radius: 12px; flex-shrink: 0;
  background: linear-gradient(145deg, #00e676, #00a844);
  display: grid; place-items: center;
  font-weight: 900; font-size: 13px; color: #031a0c; letter-spacing: -0.5px;
  box-shadow: 0 0 22px var(--green-glow);
  animation: logoPulse 3s ease-in-out infinite;
}
@keyframes logoPulse {
  0%, 100% { box-shadow: 0 0 18px var(--green-glow); }
  50% { box-shadow: 0 0 32px rgba(0,230,118,.45); }
}
.tws-brand-text { min-width: 0; }
.tws-brand-name {
  font-size: 16px; font-weight: 900; letter-spacing: 1.5px;
  background: linear-gradient(90deg, #e8f5e9, #00e676);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; line-height: 1.1;
}
.tws-brand-sub {
  font-size: 9px; color: var(--muted); letter-spacing: 2px; margin-top: 2px;
  text-transform: uppercase;
}
.tws-ticker-pill {
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
  font-size: 11px; color: var(--muted);
}
.tws-ticker-pill b { color: var(--green); font-weight: 700; }
.tws-live {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 10px; font-weight: 700; color: var(--green);
  padding: 4px 10px; border-radius: 999px;
  background: var(--green-dim); border: 1px solid rgba(0,230,118,.25);
}
.tws-live::before {
  content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--green);
  box-shadow: 0 0 8px var(--green); animation: blink 1.6s ease-in-out infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: .35; }
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070d0a, #0a1210) !important;
  border-right: 1px solid var(--border-g) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stRadio label {
  background: rgba(0,40,20,.25) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: 8px 12px !important;
  margin-bottom: 4px !important;
  transition: all .25s ease !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
  border-color: var(--green2) !important;
  background: var(--green-dim) !important;
}

.card3d {
  position: relative; overflow: hidden;
  background: linear-gradient(160deg, rgba(12,22,18,.95), rgba(8,14,12,.98));
  border: 1px solid var(--border-g);
  border-radius: 14px; padding: 14px 16px;
  box-shadow: 0 8px 28px rgba(0,0,0,.35), inset 0 1px 0 rgba(0,230,118,.06);
  transition: transform .35s cubic-bezier(.16,1,.3,1), box-shadow .35s ease, border-color .35s ease;
  transform-style: preserve-3d;
  animation: cardIn .55s cubic-bezier(.16,1,.3,1) both;
}
.card3d:hover {
  transform: translateY(-5px) rotateX(2deg);
  border-color: rgba(0,230,118,.4);
  box-shadow: 0 16px 40px rgba(0,0,0,.45), 0 0 30px rgba(0,230,118,.1);
}
.card3d::after {
  content: ""; position: absolute; inset: 0;
  background: linear-gradient(120deg, transparent 30%, rgba(0,230,118,.05) 50%, transparent 70%);
  transform: translateX(-130%); transition: transform .7s ease; pointer-events: none;
}
.card3d:hover::after { transform: translateX(130%); }
@keyframes cardIn {
  from { opacity: 0; transform: translateY(16px) scale(.97); }
  to { opacity: 1; transform: none; }
}

.metric-label {
  font-size: 10px; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; color: var(--muted);
}
.metric-val {
  font-size: clamp(16px, 2.2vw, 22px); font-weight: 800;
  margin-top: 6px; line-height: 1.2; color: var(--text);
}
.metric-sub { font-size: 10px; color: var(--muted); margin-top: 3px; }
.pos { color: var(--green) !important; }
.neg { color: var(--red) !important; }
.amber { color: var(--amber) !important; }

.lvl-call { border-color: rgba(0,230,118,.35) !important; }
.lvl-call .metric-val { color: var(--green); text-shadow: 0 0 12px rgba(0,230,118,.2); }
.lvl-put { border-color: rgba(255,82,82,.35) !important; }
.lvl-put .metric-val { color: var(--red); text-shadow: 0 0 12px rgba(255,82,82,.2); }
.lvl-flip { border-color: rgba(255,215,64,.35) !important; }
.lvl-flip .metric-val { color: var(--amber); text-shadow: 0 0 12px rgba(255,215,64,.2); }
.lvl-pain { border-color: rgba(100,180,255,.35) !important; }
.lvl-pain .metric-val { color: #82b4ff; }

.sec {
  font-size: 13px; font-weight: 800; letter-spacing: .8px;
  color: var(--green); margin: 18px 0 10px;
  display: flex; align-items: center; gap: 8px;
}
.sec::after {
  content: ""; flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(0,230,118,.3), transparent);
}

.quote-strip {
  display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;
}
.quote-chip {
  background: var(--panel); border: 1px solid var(--border-g);
  border-radius: 10px; padding: 6px 12px; font-size: 11px;
  transition: border-color .25s, transform .25s;
  animation: cardIn .4s both;
}
.quote-chip:hover { border-color: var(--green); transform: translateY(-2px); }
.quote-chip b { color: var(--text); }
.quote-chip .up { color: var(--green); }
.quote-chip .dn { color: var(--red); }

.news-item {
  padding: 12px 14px; margin-bottom: 8px; border-radius: 12px;
  background: linear-gradient(145deg, rgba(10,20,16,.95), rgba(6,12,10,.98));
  border: 1px solid var(--border);
  transition: border-color .25s, transform .25s;
  animation: cardIn .4s both;
}
.news-item:hover { border-color: var(--green2); transform: translateX(3px); }
.news-item a { color: var(--text); text-decoration: none; font-weight: 700; font-size: 13px; }
.news-item a:hover { color: var(--green); }
.news-meta { font-size: 10px; color: var(--muted); margin-top: 6px; display: flex; gap: 12px; flex-wrap: wrap; }

.stButton > button {
  width: 100%; height: 40px; border: none !important; border-radius: 10px !important;
  background: linear-gradient(90deg, #00c853, #00e676) !important;
  color: #031a0c !important; font-weight: 800 !important; font-size: 13px !important;
  transition: transform .25s ease, box-shadow .25s ease !important;
  box-shadow: 0 4px 16px rgba(0,230,118,.2) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(0,230,118,.35) !important;
}
.stButton > button:active { transform: scale(.97) !important; }

[data-testid="stDataFrame"] {
  border: 1px solid var(--border-g) !important; border-radius: 12px !important;
  overflow: hidden !important;
  box-shadow: 0 8px 24px rgba(0,0,0,.3) !important;
}

div[data-testid="stPopover"] > button {
  width: 40px !important; height: 40px !important; min-height: 40px !important;
  padding: 0 !important; border-radius: 11px !important;
  background: linear-gradient(145deg, rgba(0,230,118,.2), rgba(0,168,68,.15)) !important;
  border: 1px solid rgba(0,230,118,.35) !important;
  color: var(--green) !important; font-size: 16px !important;
  transition: all .25s ease !important;
}
div[data-testid="stPopover"] > button:hover {
  transform: translateY(-2px) scale(1.05) !important;
  box-shadow: 0 6px 20px rgba(0,230,118,.25) !important;
}

div[data-testid="stExpander"] {
  background: var(--panel) !important;
  border: 1px solid var(--border-g) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
  font-weight: 700 !important; color: var(--green) !important;
}

.tws-foot {
  text-align: center; color: var(--muted); font-size: 10px;
  padding: 20px 0 8px; letter-spacing: .5px;
}

@media (max-width: 768px) {
  .block-container { padding: 0.4rem 0.6rem 1.5rem !important; }
  .tws-top { padding: 8px 10px; border-radius: 12px; }
  .tws-logo-mark { width: 34px; height: 34px; font-size: 11px; }
  .tws-brand-name { font-size: 13px; letter-spacing: 1px; }
  .tws-brand-sub { font-size: 8px; letter-spacing: 1px; }
  .card3d { padding: 12px; border-radius: 12px; }
  .metric-val { font-size: 16px; }
  .quote-chip { font-size: 10px; padding: 5px 8px; }
}
@media (max-width: 400px) {
  .tws-brand-name { font-size: 12px; }
  .metric-val { font-size: 14px; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# STATE
# ═══════════════════════════════════════════════════════════════
DEFAULT_UNIVERSE = [
    "SPY", "QQQ", "IWM", "NVDA", "AMD", "AAPL", "TSLA", "MSFT",
    "META", "AMZN", "GOOGL", "NFLX", "AVGO", "PLTR", "SMCI", "COIN",
]
SECTOR_MAP = {
    "SPY": "Index", "QQQ": "Tech", "IWM": "SmallCap",
    "NVDA": "Semi", "AMD": "Semi", "AVGO": "Semi", "INTC": "Semi", "MU": "Semi",
    "AAPL": "Tech", "MSFT": "Tech", "GOOGL": "Tech", "META": "Tech", "NFLX": "Tech", "PLTR": "Tech",
    "TSLA": "Auto", "AMZN": "Consumer", "COIN": "Crypto", "SMCI": "Hardware",
}

if "tws_ticker" not in st.session_state:
    st.session_state.tws_ticker = "SPY"
if "module" not in st.session_state:
    st.session_state.module = "Gamma"
if "load_news" not in st.session_state:
    st.session_state.load_news = False


def normalize_symbol(value: str) -> str:
    v = value.strip().upper().replace(" ", "")
    crypto = {
        "BTC": "BTC-USD", "BITCOIN": "BTC-USD",
        "ETH": "ETH-USD", "ETHEREUM": "ETH-USD",
        "SOL": "SOL-USD", "SOLANA": "SOL-USD",
        "DOGE": "DOGE-USD", "XRP": "XRP-USD", "BNB": "BNB-USD",
    }
    return crypto.get(v, v)


# ═══════════════════════════════════════════════════════════════
# TOP BAR
# ═══════════════════════════════════════════════════════════════
bar_l, bar_r = st.columns([11, 1.1], vertical_alignment="center")
with bar_l:
    st.markdown(f"""
    <div class="tws-top">
      <div class="tws-brand-row">
        <div class="tws-logo-mark">TWS</div>
        <div class="tws-brand-text">
          <div class="tws-brand-name">TRADE WITH SOHAIB</div>
          <div class="tws-brand-sub">Learn · Analyze · Trade · Grow</div>
        </div>
      </div>
      <div class="tws-ticker-pill">
        <span class="tws-live">LIVE</span>
        <span>SELECTED <b>{st.session_state.tws_ticker}</b></span>
        <span style="opacity:.5">{datetime.now():%H:%M:%S}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with bar_r:
    with st.popover("🔍", help="Search symbol"):
        st.markdown("**Select Market**")
        sv = st.text_input("Symbol", value=st.session_state.tws_ticker, placeholder="AAPL, NVDA, SPY, BTC…", key="sym_in")
        ql = ["SPY", "QQQ", "NVDA", "AAPL", "TSLA", "MSFT", "BTC-USD", "ETH-USD"]
        cur = st.session_state.tws_ticker if st.session_state.tws_ticker in ql else "SPY"
        qk = st.selectbox("Quick", ql, index=ql.index(cur))
        a, b = st.columns(2)
        if a.button("✓ Apply", use_container_width=True):
            st.session_state.tws_ticker = normalize_symbol(sv)
            st.session_state.load_news = False
            st.cache_data.clear()
            st.rerun()
        if b.button("⚡ Quick", use_container_width=True):
            st.session_state.tws_ticker = normalize_symbol(qk)
            st.session_state.load_news = False
            st.cache_data.clear()
            st.rerun()

ticker = st.session_state.tws_ticker

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ◉ T.W.S CONTROLS")
    mods = ["Gamma", "Chart", "Volume", "Watchlist"]
    if st.session_state.module not in mods:
        st.session_state.module = "Gamma"
    module = st.radio("Module", mods, index=mods.index(st.session_state.module), label_visibility="collapsed")
    st.session_state.module = module

    st.markdown("---")
    n_exp = st.slider("Expirations", 1, 10, 5, help="Option expirations for Gamma")
    window = st.slider("Strike window ±%", 5, 40, 15)
    vol_lb = st.slider("Vol lookback (d)", 5, 40, 20)
    vol_mult = st.slider("Unusual vol ×", 1.5, 4.0, 2.0, 0.1)

    st.markdown("---")
    if st.button("📰 News for " + ticker, use_container_width=True, key="news_btn"):
        st.session_state.load_news = not st.session_state.load_news
        st.rerun()

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.load_news = False
        st.cache_data.clear()
        st.rerun()

    st.caption("Yahoo Finance · ~15m delayed · Not financial advice")

# ═══════════════════════════════════════════════════════════════
# MATH
# ═══════════════════════════════════════════════════════════════
def bs_gamma(S, K, T, sigma, r=0.0):
    S = np.asarray(S, dtype=float)
    with np.errstate(all="ignore"):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        g = np.exp(-0.5 * d1**2) / np.sqrt(2 * np.pi) / (S * sigma * np.sqrt(T))
    return np.nan_to_num(g, nan=0.0, posinf=0.0, neginf=0.0)


def total_gex_at(S, K, T, iv, oi, sign):
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


def fmt(x):
    return f"${x:,.2f}" if pd.notna(x) else "N/A"


# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════
def _clean(df):
    for c in ("openInterest", "volume", "impliedVolatility"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    df["strike"] = pd.to_numeric(df["strike"], errors="coerce")
    return df.dropna(subset=["strike"])


def load_yahoo_opts(symbol, n_exp):
    stock = yf.Ticker(symbol)
    spot = None
    try:
        spot = float(stock.fast_info["lastPrice"])
    except Exception:
        pass
    if not spot or np.isnan(spot):
        hist = stock.history(period="5d")
        if hist.empty:
            raise ValueError("No price data")
        spot = float(hist["Close"].iloc[-1])
    exps = list(stock.options)
    if not exps:
        raise ValueError("No options chain")
    rows = []
    for exp in exps[:n_exp]:
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
        raise ValueError("Empty chain")
    return spot, _clean(pd.concat(rows, ignore_index=True))


def load_cboe_opts(symbol, n_exp):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = None
    for sym in (symbol, "_" + symbol):
        url = f"https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json().get("data")
                if data and data.get("options"):
                    break
        except Exception:
            continue
    if not data or not data.get("options"):
        raise ValueError("Cboe unavailable")
    spot = float(data.get("current_price") or data.get("close") or data.get("prev_day_close"))
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
        raise ValueError("Cboe parse fail")
    df = pd.DataFrame(rows)
    today = pd.Timestamp.today().normalize()
    df = df[pd.to_datetime(df["expiration"]) >= today]
    keep = sorted(df["expiration"].unique())[:n_exp]
    return spot, _clean(df[df["expiration"].isin(keep)].reset_index(drop=True))


@st.cache_data(ttl=120, show_spinner="Loading options…")
def load_options(symbol, n_exp):
    errs = []
    for _ in range(2):
        try:
            s, d = load_yahoo_opts(symbol, n_exp)
            return s, d, "Yahoo"
        except Exception as e:
            errs.append(str(e))
            time.sleep(0.8)
    try:
        s, d = load_cboe_opts(symbol, n_exp)
        return s, d, "Cboe"
    except Exception as e:
        errs.append(str(e))
    raise ValueError(f"No options for {symbol}: " + " | ".join(dict.fromkeys(errs)))


@st.cache_data(ttl=120, show_spinner=False)
def load_quote_strip(symbols: tuple):
    rows = []
    for sym in symbols:
        try:
            h = yf.Ticker(sym).history(period="5d")
            if h is None or h.empty:
                continue
            last = float(h["Close"].iloc[-1])
            prev = float(h["Close"].iloc[-2]) if len(h) > 1 else last
            chg = (last / prev - 1) * 100 if prev else 0
            rows.append({"sym": sym, "last": last, "chg": chg})
        except Exception:
            continue
    return rows


@st.cache_data(ttl=180, show_spinner="Scanning volume…")
def scan_volume(symbols: tuple, lookback: int, mult: float):
    out = []
    for sym in symbols:
        try:
            h = yf.Ticker(sym).history(period=f"{lookback + 5}d")
            if h is None or len(h) < lookback:
                continue
            avg = float(h["Volume"].iloc[-lookback:-1].mean())
            last_v = float(h["Volume"].iloc[-1])
            last_c = float(h["Close"].iloc[-1])
            prev_c = float(h["Close"].iloc[-2]) if len(h) > 1 else last_c
            chg = (last_c / prev_c - 1) * 100 if prev_c else 0
            ratio = last_v / avg if avg > 0 else 0
            if ratio >= mult:
                out.append({
                    "Symbol": sym, "Sector": SECTOR_MAP.get(sym, "—"),
                    "Last": round(last_c, 2), "Chg %": round(chg, 2),
                    "Vol": int(last_v), "Avg Vol": int(avg),
                    "Ratio": round(ratio, 2),
                })
        except Exception:
            continue
    if not out:
        return pd.DataFrame()
    return pd.DataFrame(out).sort_values("Ratio", ascending=False).reset_index(drop=True)


@st.cache_data(ttl=90, show_spinner="Loading watchlist…")
def load_watchlist(symbols: tuple):
    rows = []
    for sym in symbols:
        try:
            h = yf.Ticker(sym).history(period="5d")
            if h is None or h.empty:
                continue
            last = float(h["Close"].iloc[-1])
            prev = float(h["Close"].iloc[-2]) if len(h) > 1 else last
            chg = (last / prev - 1) * 100 if prev else 0
            rows.append({
                "Symbol": sym, "Sector": SECTOR_MAP.get(sym, "—"),
                "Last": round(last, 2), "Chg %": round(chg, 2),
                "Volume": int(h["Volume"].iloc[-1]),
            })
        except Exception:
            continue
    return pd.DataFrame(rows) if rows else pd.DataFrame()


@st.cache_data(ttl=300, show_spinner="Fetching news…")
def load_ticker_news(symbol: str, max_n: int = 15):
    items = []
    seen = set()
    now = datetime.utcnow()
    try:
        raw = yf.Ticker(symbol).news or []
    except Exception:
        raw = []
    for n in raw:
        content = n.get("content") if isinstance(n.get("content"), dict) else None
        if content:
            title = (content.get("title") or "").strip()
            summary = (content.get("summary") or content.get("description") or "")[:240]
            pub = content.get("pubDate") or content.get("providerPublishTime")
            link = ""
            cu = content.get("clickThroughUrl") or content.get("canonicalUrl") or {}
            if isinstance(cu, dict):
                link = cu.get("url") or ""
            prov = content.get("provider")
            provider = prov.get("displayName") if isinstance(prov, dict) else (prov or "Yahoo")
        else:
            title = (n.get("title") or "").strip()
            summary = (n.get("summary") or "")[:240]
            pub = n.get("providerPublishTime")
            link = n.get("link") or n.get("url") or ""
            provider = n.get("publisher") or "Yahoo"
        if not title or title in seen:
            continue
        seen.add(title)
        ts = None
        if isinstance(pub, (int, float)):
            ts = datetime.utcfromtimestamp(pub)
        elif isinstance(pub, str):
            try:
                ts = datetime.fromisoformat(pub.replace("Z", "+00:00")).replace(tzinfo=None)
            except Exception:
                pass
        age = (now - ts).total_seconds() / 3600 if ts else None
        items.append({"title": title, "summary": summary, "provider": provider, "link": link, "age_h": age})
    items.sort(key=lambda x: x["age_h"] if x["age_h"] is not None else 9999)
    return items[:max_n]


# ═══════════════════════════════════════════════════════════════
# NEWS PANEL (only when toggled — no auto load on scroll)
# ═══════════════════════════════════════════════════════════════
if st.session_state.load_news:
    with st.expander(f"📰 News — {ticker}  (click to collapse / Close below)", expanded=True):
        news = load_ticker_news(ticker)
        if not news:
            st.info(f"No recent headlines for {ticker}.")
        else:
            for i, r in enumerate(news):
                age = f"{r['age_h']:.1f}h ago" if r.get("age_h") is not None else "—"
                title_html = (
                    f'<a href="{r["link"]}" target="_blank" rel="noopener">{r["title"]}</a>'
                    if r.get("link") else r["title"]
                )
                st.markdown(f"""
                <div class="news-item" style="animation-delay:{i*0.04}s">
                  <div>{title_html}</div>
                  <div style="color:#7a8f82;font-size:12px;margin-top:4px">{r.get("summary") or ""}</div>
                  <div class="news-meta">
                    <span>📡 {r.get("provider") or "—"}</span>
                    <span>⏱ {age}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        if st.button("✕ Close News", key="close_news", use_container_width=True):
            st.session_state.load_news = False
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# QUOTE STRIP
# ═══════════════════════════════════════════════════════════════
strip_syms = tuple(dict.fromkeys([ticker, "SPY", "QQQ", "NVDA", "BTC-USD"]))
quotes = load_quote_strip(strip_syms)
if quotes:
    chips = []
    for q in quotes:
        cls = "up" if q["chg"] >= 0 else "dn"
        chips.append(
            f'<div class="quote-chip"><b>{q["sym"]}</b> '
            f'${q["last"]:,.2f} <span class="{cls}">{q["chg"]:+.2f}%</span></div>'
        )
    st.markdown(f'<div class="quote-strip">{"".join(chips)}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# MODULE: GAMMA
# ═══════════════════════════════════════════════════════════════
def render_gamma(ticker, n_exp, window):
    try:
        spot, opt, source = load_options(ticker, n_exp)
    except Exception as e:
        st.error(f"❌ Options unavailable: {e}")
        st.info("Tip: Try SPY, QQQ, NVDA, AAPL — some tickers have limited options data.")
        return

    exp_ts = pd.to_datetime(opt["expiration"]) + pd.Timedelta(hours=20)
    days = (exp_ts - pd.Timestamp.utcnow().tz_localize(None)).dt.total_seconds() / 86400
    opt["T"] = np.maximum(days.values, 0.5) / 365.0
    opt["sign"] = np.where(opt["side"] == "CALL", 1.0, -1.0)

    valid = (opt["impliedVolatility"] > 0.01) & (opt["impliedVolatility"] < 5) & (opt["openInterest"] > 0)
    g_opt = opt[valid].copy()
    K, T, IV, OI, SG = (
        g_opt["strike"].values.astype(float),
        g_opt["T"].values,
        g_opt["impliedVolatility"].values,
        g_opt["openInterest"].values,
        g_opt["sign"].values,
    )
    g_opt["GEX"] = bs_gamma(spot, K, T, IV) * OI * 100 * spot * spot * 0.01 * SG
    net_gex = float(g_opt["GEX"].sum())

    calls = opt[opt["side"] == "CALL"]
    puts = opt[opt["side"] == "PUT"]
    c_oi = calls.groupby("strike")["openInterest"].sum()
    p_oi = puts.groupby("strike")["openInterest"].sum()
    c_above = c_oi[c_oi.index >= spot]
    p_below = p_oi[p_oi.index <= spot]
    call_wall = float((c_above if not c_above.empty else c_oi).idxmax()) if len(c_oi) else np.nan
    put_wall = float((p_below if not p_below.empty else p_oi).idxmax()) if len(p_oi) else np.nan

    grid = np.linspace(spot * 0.8, spot * 1.2, 161)
    profile = np.array([total_gex_at(s, K, T, IV, OI, SG) for s in grid])
    gamma_flip = np.nan
    cross = np.where(np.sign(profile[:-1]) * np.sign(profile[1:]) < 0)[0]
    if len(cross):
        best = min(cross, key=lambda i: abs(grid[i] - spot))
        x0, x1, y0, y1 = grid[best], grid[best + 1], profile[best], profile[best + 1]
        if y1 != y0:
            gamma_flip = float(x0 - y0 * (x1 - x0) / (y1 - y0))

    mp_rows = []
    for exp, ch in opt.groupby("expiration", sort=True):
        ch_t = ch["T"].iloc[0]
        near = ch.iloc[(ch["strike"] - spot).abs().argsort()[:6]]
        atm_iv = near.loc[near["impliedVolatility"] > 0.01, "impliedVolatility"].mean() * 100
        pc = ch.loc[ch.side == "PUT", "openInterest"].sum() / max(
            ch.loc[ch.side == "CALL", "openInterest"].sum(), 1
        )
        mp_rows.append({
            "Expiration": exp, "DTE": round(ch_t * 365, 1),
            "Max Pain": max_pain(ch),
            "ATM IV %": round(atm_iv, 2) if pd.notna(atm_iv) else np.nan,
            "P/C OI": round(pc, 2),
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

    st.markdown(f"""
    <div class="sec">GAMMA STRUCTURE — {ticker} · ${spot:,.2f} · {source}</div>
    """, unsafe_allow_html=True)

    metrics = [
        ("SPOT", fmt(spot), "", ""),
        ("CALL WALL", fmt(call_wall), "lvl-call", f"{(call_wall/spot-1)*100:+.2f}%" if pd.notna(call_wall) else ""),
        ("PUT WALL", fmt(put_wall), "lvl-put", f"{(put_wall/spot-1)*100:+.2f}%" if pd.notna(put_wall) else ""),
        ("GAMMA FLIP", fmt(gamma_flip), "lvl-flip", "GEX zero"),
        ("MAX PAIN", fmt(mp_main), "lvl-pain", "Nearest exp"),
        ("ATM IV", f"{atm_iv:.1f}%" if pd.notna(atm_iv) else "N/A", "", ""),
    ]
    cols = st.columns(6)
    for col, (lab, val, extra, sub) in zip(cols, metrics):
        col.markdown(f"""
        <div class="card3d {extra}">
          <div class="metric-label">{lab}</div>
          <div class="metric-val">{val}</div>
          <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec">KEY LEVELS</div>', unsafe_allow_html=True)
    regime = "Positive Gamma (dampening)" if net_gex > 0 else "Negative Gamma (amplifying)"
    cls = "pos" if net_gex > 0 else "neg"
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="card3d lvl-pain"><div class="metric-label">Magnetic</div><div class="metric-val">{fmt(magnetic)}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card3d lvl-call"><div class="metric-label">Call Dist</div><div class="metric-val">{(call_wall/spot-1)*100:+.2f}%</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card3d lvl-put"><div class="metric-label">Put Dist</div><div class="metric-val">{(put_wall/spot-1)*100:+.2f}%</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="card3d lvl-flip"><div class="metric-label">Net GEX / 1%</div><div class="metric-val {cls}">${net_gex/1e9:,.2f}B</div><div class="metric-sub">{regime}</div></div>', unsafe_allow_html=True)

    lo, hi = spot * (1 - window / 100), spot * (1 + window / 100)

    def rule(x, color, label):
        if pd.isna(x):
            return alt.Chart(pd.DataFrame({"x": []})).mark_rule()
        d = pd.DataFrame({"x": [x], "l": [label]})
        r = alt.Chart(d).mark_rule(color=color, strokeDash=[5, 4], size=2).encode(x="x:Q")
        t = alt.Chart(d).mark_text(color=color, align="left", dx=4, dy=-8, fontSize=11).encode(x="x:Q", text="l:N")
        return r + t

    st.markdown('<div class="sec">NET GEX BY STRIKE</div>', unsafe_allow_html=True)
    gs = g_opt.groupby("strike")["GEX"].sum().reset_index()
    gs = gs[(gs.strike >= lo) & (gs.strike <= hi)]
    gs["GEX_M"] = gs["GEX"] / 1e6
    gs["dir"] = np.where(gs["GEX_M"] >= 0, "Pos", "Neg")
    bars = alt.Chart(gs).mark_bar().encode(
        x=alt.X("strike:Q", title="Strike", scale=alt.Scale(domain=[lo, hi])),
        y=alt.Y("GEX_M:Q", title="GEX ($M)"),
        color=alt.Color("dir:N", scale=alt.Scale(domain=["Pos", "Neg"], range=["#00e676", "#ff5252"]), legend=None),
        tooltip=["strike", alt.Tooltip("GEX_M:Q", format=",.1f")],
    )
    st.altair_chart(
        (bars + rule(spot, "#ffffff", "Spot") + rule(gamma_flip, "#ffd740", "Flip")
         + rule(call_wall, "#00e676", "Call") + rule(put_wall, "#ff5252", "Put")).properties(height=300),
        use_container_width=True,
    )

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="sec">OPEN INTEREST</div>', unsafe_allow_html=True)
        oi = opt.groupby(["strike", "side"])["openInterest"].sum().reset_index()
        oi = oi[(oi.strike >= lo) & (oi.strike <= hi)]
        ch = alt.Chart(oi).mark_bar(opacity=0.9).encode(
            x=alt.X("strike:Q", scale=alt.Scale(domain=[lo, hi]), title="Strike"),
            y=alt.Y("openInterest:Q", title="OI", stack=None),
            color=alt.Color("side:N", scale=alt.Scale(domain=["CALL", "PUT"], range=["#00e676", "#ff5252"]),
                            legend=alt.Legend(orient="top", title=None)),
            tooltip=["strike", "side", "openInterest"],
        )
        st.altair_chart((ch + rule(spot, "#fff", "Spot")).properties(height=280), use_container_width=True)

    with right:
        st.markdown('<div class="sec">GEX PROFILE</div>', unsafe_allow_html=True)
        prof = pd.DataFrame({"price": grid, "GEX_M": profile / 1e6})
        line = alt.Chart(prof).mark_line(color="#00e676", size=2.5).encode(
            x=alt.X("price:Q", title="Spot", scale=alt.Scale(zero=False)),
            y=alt.Y("GEX_M:Q", title="Total GEX ($M)"),
        )
        zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#334").encode(y="y:Q")
        st.altair_chart(
            (line + zero + rule(spot, "#fff", "Spot") + rule(gamma_flip, "#ffd740", "Flip")).properties(height=280),
            use_container_width=True,
        )

    st.markdown('<div class="sec">EXPIRATION TABLE</div>', unsafe_allow_html=True)
    st.dataframe(exp_table, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec">TOP STRIKES BY OI</div>', unsafe_allow_html=True)
    top = (
        opt.pivot_table(index="strike", columns="side", values="openInterest", aggfunc="sum", fill_value=0)
        .assign(Total=lambda d: d.sum(axis=1))
        .sort_values("Total", ascending=False).head(10).reset_index()
    )
    st.dataframe(top, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# MODULE: CHART (TradingView)
# ═══════════════════════════════════════════════════════════════
def render_chart(ticker):
    st.markdown(f'<div class="sec">TECHNICAL CHART — {ticker}</div>', unsafe_allow_html=True)

    tv_map = {
        "BTC-USD": "BINANCE:BTCUSDT",
        "ETH-USD": "BINANCE:ETHUSDT",
        "SOL-USD": "BINANCE:SOLUSDT",
        "DOGE-USD": "BINANCE:DOGEUSDT",
        "XRP-USD": "BINANCE:XRPUSDT",
        "BNB-USD": "BINANCE:BNBUSDT",
    }
    tv_sym = tv_map.get(ticker, ticker)

    iv = st.radio("Timeframe", ["15", "60", "240", "D", "W"], index=3, horizontal=True,
                  format_func=lambda x: {"15": "15m", "60": "1H", "240": "4H", "D": "Daily", "W": "Weekly"}[x])

    widget = f"""
    <div style="border-radius:14px;overflow:hidden;border:1px solid #1e3d2f;
                box-shadow:0 8px 32px rgba(0,0,0,.4);background:#0b1118;">
      <div class="tradingview-widget-container" style="height:520px;">
        <div id="tv_chart" style="height:100%;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "container_id": "tv_chart",
          "width": "100%",
          "height": 520,
          "symbol": "{tv_sym}",
          "interval": "{iv}",
          "timezone": "Etc/UTC",
          "theme": "dark",
          "style": "1",
          "locale": "en",
          "toolbar_bg": "#0b1118",
          "enable_publishing": false,
          "hide_side_toolbar": false,
          "allow_symbol_change": true,
          "studies": ["RSI@tv-basicstudies", "MASimple@tv-basicstudies"],
          "backgroundColor": "#0b1118",
          "gridColor": "#1a2a22"
        }});
        </script>
      </div>
    </div>
    """
    components.html(widget, height=540)
    st.caption("Chart powered by TradingView · Change symbol inside the widget if needed")


# ═══════════════════════════════════════════════════════════════
# MODULE: VOLUME
# ═══════════════════════════════════════════════════════════════
def render_volume(lookback, mult):
    st.markdown('<div class="sec">UNUSUAL VOLUME SCANNER</div>', unsafe_allow_html=True)
    df = scan_volume(tuple(DEFAULT_UNIVERSE), lookback, mult)
    if df.empty:
        st.info(f"No names ≥ {mult}× average volume in the default universe.")
        return
    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<div class="card3d"><div class="metric-label">Hits</div><div class="metric-val">{len(df)}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="card3d"><div class="metric-label">Top Ratio</div><div class="metric-val pos">{df["Ratio"].iloc[0]:.1f}×</div><div class="metric-sub">{df["Symbol"].iloc[0]}</div></div>', unsafe_allow_html=True)
    up = int((df["Chg %"] > 0).sum())
    m3.markdown(f'<div class="card3d"><div class="metric-label">Up / Down</div><div class="metric-val"><span class="pos">{up}</span> / <span class="neg">{len(df)-up}</span></div></div>', unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True, hide_index=True, column_config={
        "Ratio": st.column_config.NumberColumn(format="%.2f×"),
        "Chg %": st.column_config.NumberColumn(format="%+.2f%%"),
        "Last": st.column_config.NumberColumn(format="$%.2f"),
    })
    if len(df) >= 2:
        ch = alt.Chart(df.head(12)).mark_bar().encode(
            x=alt.X("Ratio:Q", title="Vol ratio"),
            y=alt.Y("Symbol:N", sort="-x"),
            color=alt.condition(alt.datum.Ratio >= mult * 1.5, alt.value("#00e676"), alt.value("#ffd740")),
            tooltip=["Symbol", "Ratio", "Chg %", "Vol"],
        ).properties(height=min(320, 28 * len(df.head(12))))
        st.altair_chart(ch, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# MODULE: WATCHLIST
# ═══════════════════════════════════════════════════════════════
def render_watchlist():
    st.markdown('<div class="sec">WATCHLIST</div>', unsafe_allow_html=True)
    custom = st.text_input("Symbols (comma-separated)", value=", ".join(DEFAULT_UNIVERSE[:12]))
    symbols = tuple(normalize_symbol(s) for s in custom.split(",") if s.strip())
    if not symbols:
        st.warning("Enter at least one symbol.")
        return
    df = load_watchlist(symbols)
    if df.empty:
        st.error("Could not load quotes.")
        return
    up = int((df["Chg %"] > 0).sum())
    avg = df["Chg %"].mean()
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="card3d"><div class="metric-label">Names</div><div class="metric-val">{len(df)}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="card3d"><div class="metric-label">Up</div><div class="metric-val pos">{up}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="card3d"><div class="metric-label">Down</div><div class="metric-val neg">{len(df)-up}</div></div>', unsafe_allow_html=True)
    cls = "pos" if avg >= 0 else "neg"
    m4.markdown(f'<div class="card3d"><div class="metric-label">Avg Chg</div><div class="metric-val {cls}">{avg:+.2f}%</div></div>', unsafe_allow_html=True)

    st.dataframe(df.sort_values("Chg %", ascending=False), use_container_width=True, hide_index=True,
                 column_config={
                     "Last": st.column_config.NumberColumn(format="$%.2f"),
                     "Chg %": st.column_config.NumberColumn(format="%+.2f%%"),
                     "Volume": st.column_config.NumberColumn(format="%d"),
                 })
    ch = alt.Chart(df).mark_bar().encode(
        x=alt.X("Chg %:Q"), y=alt.Y("Symbol:N", sort="-x"),
        color=alt.condition(alt.datum["Chg %"] >= 0, alt.value("#00e676"), alt.value("#ff5252")),
        tooltip=["Symbol", "Sector", "Last", "Chg %"],
    ).properties(height=min(380, 26 * len(df)))
    st.altair_chart(ch, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════
if module == "Gamma":
    render_gamma(ticker, n_exp, window)
elif module == "Chart":
    render_chart(ticker)
elif module == "Volume":
    render_volume(vol_lb, vol_mult)
else:
    render_watchlist()

st.markdown("""
<div class="tws-foot">
  T.W.S — TRADE WITH SOHAIB · Learn · Analyze · Trade · Grow<br>
  Delayed public data · GEX assumes dealers long calls / short puts · Not financial advice
</div>
""", unsafe_allow_html=True)
