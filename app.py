import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# ============================================================
# PAGE CONFIG + CSS
# ============================================================
st.set_page_config(
    page_title="Options Market Structure Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.stApp {
    background:
        radial-gradient(circle at 10% 0%, #17295c 0%, transparent 30%),
        radial-gradient(circle at 90% 10%, #35145c 0%, transparent 28%),
        linear-gradient(135deg, #050711 0%, #090d1b 50%, #050711 100%);
    color: #f3f6ff;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070b17, #0b1020);
    border-right: 1px solid #202d50;
}
.block-container { max-width: 1500px; padding-top: 25px; padding-bottom: 50px; }
.hero {
    position: relative; overflow: hidden; padding: 26px 30px; border-radius: 22px;
    background: linear-gradient(135deg, rgba(22,34,76,.95), rgba(10,14,30,.94));
    border: 1px solid #2c3d70; box-shadow: 0 0 35px rgba(66,103,255,.15);
    margin-bottom: 20px;
}
.hero-title { font-size: 34px; font-weight: 800; letter-spacing: -1px; }
.hero-sub { color: #8f9dbc; margin-top: 6px; }
.live-badge {
    display: inline-block; padding: 5px 12px; border-radius: 999px; color: #51f2b1;
    background: rgba(25,92,69,.22); border: 1px solid #24785d;
    font-size: 11px; font-weight: 800; letter-spacing: .8px; margin-bottom: 10px;
}
.metric-card {
    min-height: 118px; padding: 18px; border-radius: 18px;
    background: linear-gradient(145deg, rgba(23,34,65,.92), rgba(9,14,28,.95));
    border: 1px solid #26365f; box-shadow: 0 10px 30px rgba(0,0,0,.25);
    transition: all .25s ease;
}
.metric-card:hover { transform: translateY(-4px); border-color: #536fd0; }
.metric-label { color: #7f8eaf; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.metric-value { color: #f8faff; font-size: 26px; font-weight: 800; margin-top: 8px; }
.metric-sub { color: #637292; font-size: 11px; margin-top: 5px; }
.section-title { font-size: 18px; font-weight: 800; margin: 26px 0 12px; color: #e5eaff; }
.level-card { padding: 18px; border-radius: 16px; background: rgba(13,19,38,.85); border: 1px solid #233256; }
.level-name { font-size: 11px; color: #7e8cac; text-transform: uppercase; letter-spacing: 1px; }
.level-price { font-size: 24px; font-weight: 800; margin-top: 6px; }
.pos { color: #3ddc97; } .neg { color: #ff5d73; }
.stButton button {
    width: 100%; height: 45px; border: none; border-radius: 11px;
    background: linear-gradient(90deg, #4168ff, #7255ff); color: white; font-weight: 800;
}
.footer { text-align: center; color: #52617e; font-size: 11px; padding-top: 30px; }
#MainMenu { visibility: hidden; } footer { visibility: hidden; }

/* ============================================================
   VIP MOTION SYSTEM — VISUAL ONLY
   Data/API/calculation code is intentionally untouched.
   ============================================================ */
.stApp{overflow-x:hidden}
.stApp:before{content:"";position:fixed;inset:-25%;pointer-events:none;z-index:0;background:radial-gradient(circle at 15% 15%,rgba(44,109,255,.10),transparent 22%),radial-gradient(circle at 85% 18%,rgba(184,65,255,.09),transparent 23%),radial-gradient(circle at 50% 90%,rgba(0,212,255,.055),transparent 25%);animation:vipAmbient 18s ease-in-out infinite alternate}
@keyframes vipAmbient{from{transform:translate3d(-1%,-1%,0) scale(1)}to{transform:translate3d(1.5%,1%,0) scale(1.04)}}
.block-container{position:relative;z-index:1;animation:vipPageIn .8s cubic-bezier(.16,1,.3,1) both}
@keyframes vipPageIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.hero{transform:perspective(1000px) translateZ(0);transition:transform .45s cubic-bezier(.16,1,.3,1),box-shadow .45s ease,border-color .45s ease;isolation:isolate}
.hero:before{content:"";position:absolute;inset:-2px;background:linear-gradient(110deg,transparent 25%,rgba(255,255,255,.13) 50%,transparent 75%);transform:translateX(-120%);animation:vipSheen 6s ease-in-out infinite;pointer-events:none;z-index:-1}
.hero:after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 78% 50%,rgba(110,120,255,.12),transparent 32%);animation:vipPulse 4s ease-in-out infinite alternate;pointer-events:none}
.hero:hover{transform:perspective(1000px) rotateX(.7deg) translateY(-3px);box-shadow:0 25px 65px rgba(55,88,255,.16),inset 0 1px rgba(255,255,255,.06);border-color:#40599a}
@keyframes vipSheen{0%,55%{transform:translateX(-120%)}75%,100%{transform:translateX(120%)}}
@keyframes vipPulse{from{opacity:.45}to{opacity:1}}
.live-badge{box-shadow:0 0 0 rgba(81,242,177,0);animation:vipLive 2.2s ease-in-out infinite}
@keyframes vipLive{50%{box-shadow:0 0 22px rgba(81,242,177,.12)}}
.metric-card,.level-card{position:relative;overflow:hidden;transform:translateZ(0);transition:transform .38s cubic-bezier(.16,1,.3,1),border-color .38s ease,box-shadow .38s ease,background .38s ease}
.metric-card:before,.level-card:before{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 25%,rgba(255,255,255,.07) 50%,transparent 75%);transform:translateX(-130%);transition:transform .7s ease;pointer-events:none}
.metric-card:hover:before,.level-card:hover:before{transform:translateX(130%)}
.metric-card:hover,.level-card:hover{transform:translateY(-6px) scale(1.012) perspective(700px) rotateX(1deg);box-shadow:0 18px 42px rgba(0,0,0,.35),inset 0 1px rgba(255,255,255,.05)}
.metric-value,.level-price{transition:transform .35s ease,text-shadow .35s ease,color .35s ease}
.metric-card:hover .metric-value,.level-card:hover .level-price{transform:translateX(2px);text-shadow:0 0 22px currentColor}
/* Distinct institutional colours for the key levels. */
.level-card.level-call{border-color:rgba(61,220,151,.32);background:linear-gradient(145deg,rgba(13,58,48,.52),rgba(9,14,28,.96))}
.level-card.level-call .level-price{color:#3ddc97;text-shadow:0 0 14px rgba(61,220,151,.16)}
.level-card.level-put{border-color:rgba(255,93,115,.32);background:linear-gradient(145deg,rgba(67,22,36,.48),rgba(9,14,28,.96))}
.level-card.level-put .level-price{color:#ff5d73;text-shadow:0 0 14px rgba(255,93,115,.16)}
.level-card.level-flip{border-color:rgba(255,209,102,.34);background:linear-gradient(145deg,rgba(74,58,20,.42),rgba(9,14,28,.96))}
.level-card.level-flip .level-price{color:#ffd166;text-shadow:0 0 14px rgba(255,209,102,.16)}
.level-card.level-pain{border-color:rgba(120,137,255,.34);background:linear-gradient(145deg,rgba(31,35,78,.48),rgba(9,14,28,.96))}
.level-card.level-pain .level-price{color:#9aa7ff;text-shadow:0 0 14px rgba(120,137,255,.16)}
[data-testid="stDataFrame"]{border:1px solid #243354;border-radius:15px;overflow:hidden;box-shadow:0 15px 40px rgba(0,0,0,.2);animation:vipTableIn .8s .15s both}
@keyframes vipTableIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
[data-testid="stDataFrame"] *{transition:background-color .2s ease}
.stButton button{position:relative;overflow:hidden;transform:translateZ(0);transition:transform .28s cubic-bezier(.16,1,.3,1),box-shadow .35s ease,filter .35s ease}
.stButton button:before{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 25%,rgba(255,255,255,.22) 50%,transparent 75%);transform:translateX(-130%);animation:vipButtonShine 5s ease-in-out infinite}
.stButton button:hover{transform:translateY(-3px) scale(1.01);box-shadow:0 12px 30px rgba(65,104,255,.28);filter:brightness(1.1)}
.stButton button:active{transform:translateY(0) scale(.985)}
@keyframes vipButtonShine{0%,62%{transform:translateX(-130%)}82%,100%{transform:translateX(130%)}}
section[data-testid="stSidebar"]{transition:box-shadow .5s ease,transform .45s ease}
section[data-testid="stSidebar"]:hover{box-shadow:8px 0 45px rgba(45,78,170,.12)}
/* Desktop = spacious 3D terminal feel; mobile = compact touch-first hierarchy. */
@media (min-width:1100px){
 .block-container{padding-left:34px;padding-right:34px}
 .hero{min-height:155px;display:flex;flex-direction:column;justify-content:center}
 .metric-card{min-height:128px}
 .level-card{min-height:112px}
}
@media (max-width:1099px){
 .hero-title{font-size:29px}
 .metric-card{min-height:105px;padding:15px}
 .metric-value{font-size:23px}
}
@media (max-width:700px){
 .block-container{padding:10px 10px 34px}
 .hero{padding:20px 17px;border-radius:18px;margin-bottom:14px}
 .hero-title{font-size:22px;line-height:1.15}
 .hero-sub{font-size:11px;line-height:1.5}
 .live-badge{font-size:9px;padding:4px 9px}
 .metric-card{min-height:94px;padding:13px;border-radius:14px}
 .metric-label{font-size:9px}.metric-value{font-size:20px;margin-top:6px}.metric-sub{font-size:9px}
 .level-card{padding:14px;border-radius:14px;min-height:92px}
 .level-price{font-size:20px}
 .section-title{font-size:15px;margin:19px 0 9px}
 .stDataFrame{font-size:10px}
}
@media (max-width:430px){
 .hero-title{font-size:19px}
 .metric-card{padding:11px;min-height:88px}
 .metric-value{font-size:18px}
 .level-card{padding:12px}
 .level-price{font-size:18px}
}
@media (prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}

</style>
""", unsafe_allow_html=True)

TICKERS = ["SPY", "QQQ", "IWM", "NVDA", "AMD", "AAPL", "TSLA", "MSFT", "META", "AMZN",
           "GOOGL", "NFLX", "AVGO", "INTC", "MU", "PLTR", "SMCI", "SMH", "SOXL", "COIN"]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## ⚡ OPTIONS TERMINAL")
    ticker = st.selectbox("Ticker", TICKERS, index=0)
    custom = st.text_input("Custom ticker", placeholder="Example: MSTR")
    if custom.strip():
        ticker = custom.strip().upper()
    n_exp = st.slider("Expirations to load", 1, 12, 6)
    window = st.slider("Strike window around spot (±%)", 5, 40, 15)
    st.markdown("---")
    if st.button("🚀 ANALYZE / REFRESH"):
        st.cache_data.clear()
    st.caption("Data: Yahoo Finance (yfinance), ~15 min delayed. "
               "GEX = estimate from public open interest, assuming dealers are long calls / short puts.")

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
  <div class="live-badge">● LIVE OPTIONS DATA</div>
  <div class="hero-title">Options Market Structure Terminal</div>
  <div class="hero-sub">Call Wall · Put Wall · Gamma Flip · Max Pain · IV · GEX</div>
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
import time
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
    color=alt.Color("dir:N", scale=alt.Scale(domain=["Positive", "Negative"], range=["#3ddc97", "#ff5d73"]), legend=None),
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
        color=alt.Color("side:N", scale=alt.Scale(domain=["CALL", "PUT"], range=["#3ddc97", "#ff5d73"]),
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
