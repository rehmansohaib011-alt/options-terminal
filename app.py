import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime
import re
import time
import requests

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="T.W.S GAMMA TERMINAL",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS — smooth, responsive, GPU-friendly
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    font-family: 'Inter', sans-serif;
    overflow-x: hidden !important;
    max-width: 100vw;
}
.stApp {
    background:
        radial-gradient(circle at 10% 0%, #17295c 0%, transparent 30%),
        radial-gradient(circle at 90% 10%, #35145c 0%, transparent 28%),
        linear-gradient(135deg, #050711 0%, #090d1b 50%, #050711 100%);
    color: #f3f6ff;
    -webkit-font-smoothing: antialiased;
}
img, svg, video, canvas { max-width: 100%; height: auto; }

/* ---------- Command bar ---------- */
.tws-command{
    position:relative; display:flex; align-items:center; justify-content:space-between;
    gap:12px; padding:12px 14px; margin-bottom:14px; border-radius:16px;
    background:linear-gradient(135deg,rgba(13,20,38,.92),rgba(7,11,22,.94));
    border:1px solid #26385d; box-shadow:0 14px 38px rgba(0,0,0,.22);
    overflow:hidden; min-width:0;
}
.tws-brand{ display:flex; align-items:center; gap:10px; min-width:0; flex:1 1 auto; }
.tws-mark{
    flex:0 0 auto; width:34px; height:34px; border-radius:11px;
    display:grid; place-items:center; font-weight:900; color:#fff; font-size:14px;
    background:linear-gradient(145deg,#6d5cff,#2e7bff);
    box-shadow:0 0 22px rgba(75,100,255,.28);
}
.tws-brand-text{ min-width:0; overflow:hidden; }
.tws-title{
    font-size:14px; font-weight:900; letter-spacing:.6px; line-height:1.15;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.tws-caption{
    font-size:9px; color:#71819e; margin-top:3px; letter-spacing:1px;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.tws-current{
    color:#9aa8c0; font-size:11px; flex:0 0 auto; max-width:45%;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.tws-current b{ color:#fff; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070b17, #0b1020);
    border-right: 1px solid #202d50;
}

.block-container {
    max-width: 1500px;
    padding: 20px 22px 46px;
    overflow-x: clip;
}

/* ---------- Hero ---------- */
.hero {
    position: relative; overflow: hidden;
    padding: 24px 26px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(22,34,76,.95), rgba(10,14,30,.94));
    border: 1px solid #2c3d70;
    box-shadow: 0 0 35px rgba(66,103,255,.15);
    margin-bottom: 20px;
    will-change: transform;
    transform: translateZ(0);
    transition: transform .5s cubic-bezier(.16,1,.3,1), box-shadow .5s ease, border-color .5s ease;
}
.hero::after{
    content:""; position:absolute; inset:0;
    background:radial-gradient(circle at 78% 50%,rgba(110,120,255,.14),transparent 34%);
    opacity:.5; pointer-events:none;
    animation: heroPulse 6s ease-in-out infinite alternate;
}
@keyframes heroPulse { from{opacity:.35} to{opacity:.95} }
.hero:hover{
    transform: translate3d(0,-3px,0);
    box-shadow: 0 22px 55px rgba(55,88,255,.18), inset 0 1px rgba(255,255,255,.06);
    border-color:#40599a;
}
.hero-title {
    font-size: clamp(20px, 5vw, 34px);
    font-weight: 800; letter-spacing: -0.5px; line-height: 1.15;
    word-break: break-word;
}
.hero-sub {
    color: #8f9dbc; margin-top: 8px;
    font-size: clamp(11px, 2.4vw, 14px);
    line-height: 1.5; word-break: break-word;
}
.live-badge {
    display: inline-block; padding: 5px 12px; border-radius: 999px;
    color: #51f2b1; background: rgba(25,92,69,.22); border: 1px solid #24785d;
    font-size: 11px; font-weight: 800; letter-spacing: .8px; margin-bottom: 10px;
    animation: liveGlow 2.4s ease-in-out infinite;
}
@keyframes liveGlow { 50% { box-shadow: 0 0 22px rgba(81,242,177,.18); } }

/* ---------- Metric / Level cards ---------- */
.metric-card, .level-card {
    position: relative; overflow: hidden; min-width: 0;
    padding: 16px; border-radius: 16px;
    background: linear-gradient(145deg, rgba(23,34,65,.92), rgba(9,14,28,.95));
    border: 1px solid #26365f;
    box-shadow: 0 10px 30px rgba(0,0,0,.25);
    will-change: transform; transform: translateZ(0);
    transition: transform .4s cubic-bezier(.16,1,.3,1), border-color .4s ease, box-shadow .4s ease;
}
.metric-card { min-height: 118px; }
.metric-card::before, .level-card::before{
    content:""; position:absolute; inset:0;
    background:linear-gradient(115deg,transparent 25%,rgba(255,255,255,.07) 50%,transparent 75%);
    transform: translate3d(-130%,0,0); transition: transform .8s ease; pointer-events:none;
}
.metric-card:hover::before, .level-card:hover::before{ transform: translate3d(130%,0,0); }
.metric-card:hover, .level-card:hover{
    transform: translate3d(0,-5px,0);
    border-color:#536fd0;
    box-shadow: 0 18px 42px rgba(0,0,0,.35), inset 0 1px rgba(255,255,255,.05);
}
.metric-label{
    color:#7f8eaf; font-size:10.5px; font-weight:700; letter-spacing:1px;
    text-transform:uppercase; word-break:break-word;
}
.metric-value{
    color:#f8faff; font-size: clamp(18px, 3.5vw, 26px); font-weight:800;
    margin-top:8px; word-break:break-word; line-height:1.15;
}
.metric-sub{
    color:#637292; font-size:10.5px; margin-top:5px;
    word-break:break-word; line-height:1.35;
}
.section-title{
    font-size: clamp(15px, 2.6vw, 18px);
    font-weight:800; margin:24px 0 12px; color:#e5eaff;
    word-break:break-word;
}
.level-card { padding: 16px; min-height: 110px; }
.level-name{
    font-size: 10.5px; color:#7e8cac; text-transform:uppercase;
    letter-spacing:1px; word-break:break-word;
}
.level-price{
    font-size: clamp(18px, 3.4vw, 24px); font-weight:800; margin-top:6px;
    word-break:break-word; line-height:1.15;
}
.level-card.level-call{
    border-color:rgba(61,220,151,.32);
    background:linear-gradient(145deg,rgba(13,58,48,.52),rgba(9,14,28,.96));
}
.level-card.level-call .level-price{ color:#3ddc97; }
.level-card.level-put{
    border-color:rgba(255,93,115,.32);
    background:linear-gradient(145deg,rgba(67,22,36,.48),rgba(9,14,28,.96));
}
.level-card.level-put .level-price{ color:#ff5d73; }
.level-card.level-flip{
    border-color:rgba(255,209,102,.34);
    background:linear-gradient(145deg,rgba(74,58,20,.42),rgba(9,14,28,.96));
}
.level-card.level-flip .level-price{ color:#ffd166; }
.level-card.level-pain{
    border-color:rgba(120,137,255,.34);
    background:linear-gradient(145deg,rgba(31,35,78,.48),rgba(9,14,28,.96));
}
.level-card.level-pain .level-price{ color:#9aa7ff; }

.pos { color: #3ddc97; }
.neg { color: #ff5d73; }

/* ---------- Buttons ---------- */
.stButton button{
    width: 100%; height: 44px; border: none; border-radius: 11px;
    background: linear-gradient(90deg, #4168ff, #7255ff);
    color: white; font-weight: 800;
    will-change: transform; transform: translateZ(0);
    transition: transform .28s cubic-bezier(.16,1,.3,1), box-shadow .3s ease, filter .3s ease;
}
.stButton button:hover{
    transform: translate3d(0,-2px,0);
    box-shadow: 0 10px 26px rgba(65,104,255,.28);
    filter: brightness(1.08);
}
.stButton button:active{ transform: translate3d(0,0,0) scale(.985); }

/* ---------- Dataframe ---------- */
[data-testid="stDataFrame"]{
    border:1px solid #243354; border-radius:15px; overflow:hidden;
    box-shadow:0 15px 40px rgba(0,0,0,.2); max-width:100%;
}

/* ---------- Popover (search icon) ---------- */
div[data-testid="stPopover"] > button{
    height: 42px !important; min-width: 42px !important;
    width: 42px !important; padding: 0 !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, rgba(23,34,65,.95), rgba(9,14,28,.95)) !important;
    border: 1px solid #2c3d70 !important;
    color: #c9d4ee !important;
    font-size: 16px !important; font-weight: 700;
    transition: transform .25s ease, box-shadow .3s ease, border-color .3s ease;
}
div[data-testid="stPopover"] > button:hover{
    transform: translate3d(0,-2px,0);
    border-color: #536fd0 !important;
    box-shadow: 0 10px 24px rgba(65,104,255,.22);
}

.footer {
    text-align: center; color:#52617e; font-size:11px;
    padding-top: 30px; line-height:1.6;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ---------- Responsive ---------- */
@media (min-width: 1100px){
    .block-container { padding: 26px 34px 55px; }
    .hero { min-height: 155px; display:flex; flex-direction:column; justify-content:center; }
    .metric-card { min-height: 128px; }
    .level-card { min-height: 118px; }
}
@media (max-width: 900px){
    .block-container { padding: 16px 16px 40px; }
    .hero { padding: 20px 20px; }
}
@media (max-width: 700px){
    .block-container { padding: 12px 12px 34px; }
    .hero { padding: 18px 16px; border-radius: 18px; margin-bottom: 14px; }
    .metric-card { min-height: 96px; padding: 13px; border-radius: 14px; }
    .level-card { padding: 13px; border-radius: 14px; min-height: 96px; }
    .section-title { margin: 18px 0 9px; }
    .tws-title { font-size: 12.5px; }
    .tws-caption { font-size: 8px; letter-spacing: .6px; }
    .tws-current { font-size: 10px; }
    .tws-mark { width: 30px; height: 30px; border-radius: 9px; font-size: 12px; }
}
@media (max-width: 520px){
    .tws-current { display: none; }
    .tws-command { padding: 10px 12px; }
}
@media (max-width: 430px){
    .metric-card { padding: 11px; min-height: 88px; }
    .level-card { padding: 11px; min-height: 88px; }
    .hero { padding: 16px 13px; }
}
@media (prefers-reduced-motion: reduce){
    *, *::before, *::after{
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
    }
}
</style>
""", unsafe_allow_html=True)

TICKERS = ["SPY", "QQQ", "IWM", "NVDA", "AMD", "AAPL", "TSLA", "MSFT", "META", "AMZN",
           "GOOGL", "NFLX", "AVGO", "INTC", "MU", "PLTR", "SMCI", "SMH", "SOXL", "COIN"]

# ============================================================
# SESSION STATE
# ============================================================
if "tws_ticker" not in st.session_state:
    st.session_state.tws_ticker = "SPY"

def normalize_symbol(value: str) -> str:
    value = value.strip().upper().replace(" ", "")
    crypto = {"BTC":"BTC-USD","BITCOIN":"BTC-USD","ETH":"ETH-USD","ETHEREUM":"ETH-USD",
              "SOL":"SOL-USD","SOLANA":"SOL-USD","DOGE":"DOGE-USD","DOGECOIN":"DOGE-USD",
              "XRP":"XRP-USD","BNB":"BNB-USD"}
    return crypto.get(value, value)

# ============================================================
# COMMAND BAR + SEARCH POPOVER
# ============================================================
bar_left, bar_right = st.columns([11, 1], vertical_alignment="center")

with bar_left:
    st.markdown(f"""
    <div class="tws-command">
      <div class="tws-brand">
        <div class="tws-mark">T</div>
        <div class="tws-brand-text">
          <div class="tws-title">T.W.S GAMMA TERMINAL</div>
          <div class="tws-caption">OPTIONS MARKET INTELLIGENCE</div>
        </div>
      </div>
      <div class="tws-current">SELECTED&nbsp; <b>{st.session_state.tws_ticker}</b></div>
    </div>
    """, unsafe_allow_html=True)

with bar_right:
    with st.popover("🔎", use_container_width=True):
        st.markdown("##### 🔎 Select Market")
        search_value = st.text_input(
            "Stock / Crypto / ETF",
            value=st.session_state.tws_ticker,
            placeholder="AAPL, NVDA, SPY, BTC, ETH…",
            key="tws_symbol_input",
            label_visibility="collapsed",
        )
        quick_list = ["SPY","QQQ","NVDA","AAPL","TSLA","MSFT","BTC-USD","ETH-USD"]
        current = st.session_state.tws_ticker if st.session_state.tws_ticker in quick_list else "SPY"
        quick = st.selectbox("Quick select", quick_list, index=quick_list.index(current))
        c1, c2 = st.columns(2)
        if c1.button("✓ Apply", use_container_width=True):
            new_sym = normalize_symbol(search_value)
            if new_sym and new_sym != st.session_state.tws_ticker:
                st.session_state.tws_ticker = new_sym
                st.cache_data.clear()
                st.rerun()
        if c2.button("⚡ Quick", use_container_width=True):
            new_sym = normalize_symbol(quick)
            if new_sym and new_sym != st.session_state.tws_ticker:
                st.session_state.tws_ticker = new_sym
                st.cache_data.clear()
                st.rerun()

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
with st.sidebar:
    st.markdown("## ⚡ TERMINAL CONTROLS")
    n_exp = st.slider("Expirations to load", 1, 12, 6)
    window = st.slider("Strike window around spot (±%)", 5, 40, 15)
    debug_mode = st.checkbox("🐞 Debug mode (show errors)", value=False)
    st.markdown("---")
    if st.button("🚀 ANALYZE / REFRESH"):
        st.cache_data.clear()
        st.rerun()
    st.caption("Data: Yahoo Finance (yfinance), ~15 min delayed. GEX = estimate from public open interest, assuming dealers are long calls / short puts.")

ticker = st.session_state.tws_ticker

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
# MATH
# ============================================================
def bs_gamma(S, K, T, sigma, r=0.0):
    S = np.asarray(S, dtype=float)
    with np.errstate(all="ignore"):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        g = np.exp(-0.5 * d1 ** 2) / np.sqrt(2 * np.pi) / (S * sigma * np.sqrt(T))
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


# ============================================================
# DATA LOADERS
# ============================================================
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
        raise ValueError("Yahoo: no options listed")

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
    for sym in (symbol, "_" + symbol):
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


@st.cache_data(ttl=180, show_spinner=False)
def load_options(symbol, n_exp):
    errors = []
    for attempt in range(2):
        try:
            spot, df = load_yahoo(symbol, n_exp)
            return spot, df, "Yahoo Finance"
        except Exception as e:
            errors.append(f"Yahoo#{attempt+1}: {e}")
            time.sleep(0.6)
    try:
        spot, df = load_cboe(symbol, n_exp)
        return spot, df, "Cboe (delayed)"
    except Exception as e:
        errors.append(f"Cboe: {e}")
    raise ValueError(" | ".join(dict.fromkeys(errors)))


# ============================================================
# FETCH + ANALYSIS (fully wrapped)
# ============================================================
with st.status("📡 Fetching option chain…", expanded=True) as status:
    st.write(f"Trying **Yahoo Finance** for `{ticker}` ({n_exp} expirations)…")
    try:
        spot, opt, source = load_options(ticker, n_exp)
        status.update(label=f"✅ Data loaded from {source}", state="complete", expanded=False)
    except Exception as fetch_err:
        status.update(label="❌ Data fetch failed", state="error", expanded=True)
        st.error(f"**Data fetch error:** {fetch_err}")
        if debug_mode:
            import traceback
            st.code(traceback.format_exc())
        st.info("💡 Try SPY / QQQ / AAPL. Yahoo kabhi kabhi rate-limit karta hai — 30 sec baad REFRESH dabao.")
        st.stop()

st.caption(f"Fetched {len(opt):,} option rows · Spot ${spot:,.2f} · Source: {source}")

try:
    # ---- time to expiry (pandas-safe) ----
    exp_ts = pd.to_datetime(opt["expirati
