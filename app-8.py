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

.tws-logo-img {
  width: 48px; height: 48px; border-radius: 12px; object-fit: cover;
  box-shadow: 0 0 22px var(--green-glow);
  border: 1px solid rgba(0,230,118,.35);
  flex-shrink: 0;
  animation: logoPulse 3s ease-in-out infinite;
}
.tws-search-wrap {
  display: flex; gap: 8px; align-items: center; margin-bottom: 12px;
  flex-wrap: wrap;
}
/* Mobile: hide long brand sub if needed */
@media (max-width: 768px) {
  .tws-logo-img { width: 40px; height: 40px; border-radius: 10px; }
  .tws-brand-sub { display: none; }
  /* News button prominence on mobile */
  section[data-testid="stSidebar"] .stButton:has(button[kind="secondary"]) button,
  section[data-testid="stSidebar"] button {
    min-height: 44px !important;
  }
}

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
  
.tws-logo-img {
  width: 48px; height: 48px; border-radius: 12px; object-fit: cover;
  box-shadow: 0 0 22px var(--green-glow);
  border: 1px solid rgba(0,230,118,.35);
  flex-shrink: 0;
  animation: logoPulse 3s ease-in-out infinite;
}
.tws-search-wrap {
  display: flex; gap: 8px; align-items: center; margin-bottom: 12px;
  flex-wrap: wrap;
}
/* Mobile: hide long brand sub if needed */
@media (max-width: 768px) {
  .tws-logo-img { width: 40px; height: 40px; border-radius: 10px; }
  .tws-brand-sub { display: none; }
  /* News button prominence on mobile */
  section[data-testid="stSidebar"] .stButton:has(button[kind="secondary"]) button,
  section[data-testid="stSidebar"] button {
    min-height: 44px !important;
  }
}

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
        <img class="tws-logo-img" src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAAAIYAAAAAAIQAABtbnRyUkdCIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAAAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAAAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3BhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADTLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAwADEANv/bAEMACAYGBwYFCAcHBwkJCAoMFA0MCwsMGRITDxQdGh8eHRocHCAkLicgIiwjHBwoNyksMDE0NDQfJzk9ODI8LjM0Mv/bAEMBCQkJDAsMGA0NGDIhHCEyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMv/AABEICLwD7gMBIgACEQEDEQH/xAAcAAEAAAcBAAAAAAAAAAAAAAAAAQIDBAUGBwj/xABXEAEAAQMCAwQDCwcICAQFAwUAAQIDBAURBhIhBzFBURNhcRQVFiIyVFWBkZLRI0KTlKGxwQgXMzREUmJyJDVDRVNzguEYJWN0NoOy8PEmJzdkolajwv/EABsBAQACAwEBAAAAAAAAAAAAAAABAwIEBQYH/8QAMREBAAICAQQBBAAEBgMBAQAAAAECAxEEBRIhMUETIjJRFCMzYRVCUnGBkSRDsWKh/9oADAMBAAIRAxEAPwDz+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgDEjLfBfiH6C1P9UufgfBfiH6C1P8AVLn4AxIy3wX4h+gtT/VLn4HwX4h+gtT/AFS5+AMSMt8F+IfoLU/1S5+B8F+IfoLU/wBUufgD3SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAp5E3Ixrs2Y3uxRPJH+LboqAOD5l3KuZl2rLruTfmqefnmd91Dmq85+13mvFx7lU1V2LVVU98zREyh7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/ac1XnP2u8e4sX5tZ/Rwe4sX5tZ/RwDg/NV5z9pzVec/a7x7ixfm1n9HB7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/ac1XnP2u8e4sX5tZ/Rwe4sX5tZ/RwDg/NV5z9pzVec/a7x7ixfm1n9HB7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/ac1XnP2u8e4sX5tZ/Rwe4sX5tZ/RwDg/NV5z9pzVec/a7x7ixfm1n9HB7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/ac1XnP2u8e4sX5tZ/Rwe4sX5tZ/RwDg/NV5z9pzVec/a7x7ixfm1n9HB7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/ac1XnP2u8e4sX5tZ/Rwe4sX5tZ/RwDg/NV5z9pzVec/a7x7ixfm1n9HB7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/ac1XnP2u8e4sX5tZ/Rwe4sX5tZ/RwDg/NV5z9pzVec/a7x7ixfm1n9HB7ixfm1n9HAOD81XnP2nNV5z9rvHuLF+bWf0cHuLF+bWf0cA4PzVec/a2Hgu7nU8R49OLVcm3VVteiPk8vju6v7ixfm1n9HCe3Ys2ZmbdqiiZ7+WmIBUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/9k=" alt="TWS" />
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

# Compact search row under brand (works well on mobile + desktop)
with st.form("tws_search_form", clear_on_submit=False):
    sc1, sc2, sc3 = st.columns([4, 1.2, 1.2])
    with sc1:
        form_sym = st.text_input(
            "Search",
            value=st.session_state.tws_ticker,
            placeholder="Search symbol… SPY, NVDA, BTC, AAPL",
            label_visibility="collapsed",
            key="form_sym",
        )
    with sc2:
        go = st.form_submit_button("Search", use_container_width=True)
    with sc3:
        # quick jump to chart module after search is handled below
        pass
    if go and form_sym.strip():
        st.session_state.tws_ticker = normalize_symbol(form_sym)
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
    st.markdown('<div class="sec" style="margin-top:4px">NEWS</div>', unsafe_allow_html=True)
    if st.button(f"📰 {ticker} News", use_container_width=True, key="news_btn"):
        st.session_state.load_news = not st.session_state.load_news
        st.rerun()
    st.caption("Opens popup for selected symbol only. Close when done.")

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
    with st.expander(f"📰 {ticker} — Related News (tap header to collapse)", expanded=True):
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
