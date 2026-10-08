import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timezone
import time, re, requests, xml.etree.ElementTree as ET, html as html_lib, base64, math
from urllib.parse import quote_plus

st.set_page_config(page_title="T.W.S GAMMA TERMINAL", page_icon="TWS", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# BRAND ASSET — user's TWS / Trade With Sohaib logo
# ============================================================
LOGO_PATH = "/mnt/data/tws_logo_clean.jpg"
try:
    with open(LOGO_PATH, "rb") as f:
        LOGO_B64 = base64.b64encode(f.read()).decode()
except Exception:
    LOGO_B64 = ""

# ============================================================
# PREMIUM RESPONSIVE UI
# ============================================================
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
:root{--bg:#02070a;--panel:#061116;--panel2:#08171d;--line:#12333b;--green:#46ff91;--green2:#00d66f;--red:#ff4e70;--gold:#f2c85b;--text:#e7f5f0;--muted:#70868d;--cyan:#53dfff}
html,body,[class*="css"]{font-family:Inter,system-ui,sans-serif}
.stApp{background:radial-gradient(circle at 50% -10%,#08221d 0,#02070a 38%,#010407 100%);color:var(--text)}
.block-container{max-width:1800px;padding:18px 18px 80px!important}
header[data-testid="stHeader"]{background:transparent!important}
#MainMenu,footer{visibility:hidden}
section[data-testid="stSidebar"]{background:#02080b!important;border-right:1px solid #12333b!important}
section[data-testid="stSidebar"] .block-container{padding:18px!important}
.stButton>button,.stDownloadButton>button{border:1px solid #17404a!important;background:linear-gradient(180deg,#0a1b21,#061116)!important;color:#dceee8!important;border-radius:9px!important;font-weight:700!important;transition:.2s!important}
.stButton>button:hover{border-color:var(--green)!important;box-shadow:0 0 18px #00ff7730!important;transform:translateY(-1px)!important}
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div{background:#061116!important;border:1px solid #17404a!important;color:#e7f5f0!important;border-radius:9px!important}
[data-testid="stPopover"]>button{border:1px solid #17404a!important;background:#061116!important;border-radius:10px!important}
[data-testid="stMetric"]{background:#061116;border:1px solid #12333b;border-radius:12px;padding:12px}
[data-testid="stDataFrame"]{border:1px solid #12333b;border-radius:12px;overflow:hidden}
[data-testid="stExpander"]{border:1px solid #12333b!important;background:#061116!important;border-radius:12px!important}

/* Header */
.tws-header{display:flex;align-items:center;gap:16px;border:1px solid #16414a;border-radius:16px;background:linear-gradient(100deg,#061116,#071b18,#061116);padding:10px 14px;box-shadow:0 0 35px #00ff7710;position:relative;overflow:hidden}
.tws-header:after{content:"";position:absolute;inset:-2px;background:linear-gradient(90deg,transparent,#45ff8a22,transparent);transform:translateX(-100%);animation:sweep 5s linear infinite;pointer-events:none}
@keyframes sweep{to{transform:translateX(100%)}}
.tws-logo{width:92px;height:62px;object-fit:contain;border-radius:10px;background:#000;flex:none}
.brand{min-width:220px}.brand-title{font-weight:900;letter-spacing:.6px;font-size:18px}.brand-title span{color:var(--green)}.brand-sub{font-family:'Space Mono';font-size:8px;letter-spacing:2px;color:#6f878d;margin-top:4px}
.search-box{height:44px;border:1px solid #1d5661;border-radius:11px;background:#041014;display:flex;align-items:center;padding:0 12px;gap:10px;color:#7f969c;font-size:11px;box-shadow:inset 0 0 20px #0008}.search-icon{font-size:20px;color:#d9f8ee}.kbd{margin-left:auto;border:1px solid #1b3f47;border-radius:5px;padding:4px 7px;font:9px 'Space Mono';color:#6d858b}
.ticker-strip{display:flex;gap:7px;margin-left:auto}.ticker{border:1px solid #153941;background:#061116;border-radius:9px;padding:7px 9px;min-width:80px;font-size:8px;color:#789097}.ticker b{display:block;color:#e7f5f0;font-size:10px}.up{color:var(--green)!important}.down{color:var(--red)!important}

/* Layout */
.nav-card,.news-card-wrap,.panel,.hero,.quote{border:1px solid #12333b;background:linear-gradient(180deg,#07161b,#040c10);border-radius:15px;box-shadow:0 12px 35px #0008}
.nav-card{padding:12px;position:sticky;top:12px}.nav-logo{width:100%;height:95px;object-fit:contain;background:#000;border-radius:12px;margin-bottom:8px}.nav-section{font:700 9px 'Space Mono';color:#8bffb5;letter-spacing:1.5px;margin:15px 4px 6px}.nav-btn{width:100%;padding:10px 11px;border-radius:9px;margin:3px 0;background:transparent;color:#91a5aa;font-size:11px;text-align:left;border:1px solid transparent}.nav-btn.active,.nav-btn:hover{background:linear-gradient(90deg,#063d24,#07151a);color:#eafff4;border-color:#1c774f;box-shadow:0 0 15px #00ff7718}
.hero{padding:20px;margin-bottom:12px;background:radial-gradient(circle at 90% 10%,#0a3c2a,#07151a 55%,#040b0f)}.live-pill{display:inline-block;border:1px solid #167b50;background:#06251a;color:#5cff9d;border-radius:20px;padding:5px 9px;font:700 8px 'Space Mono';letter-spacing:1px}.hero h1{font-size:29px;margin:13px 0 5px;letter-spacing:-1px}.hero p{margin:0;color:#71878c;font-size:9px;letter-spacing:1.4px}.quote{padding:12px 14px;display:flex;align-items:center;gap:13px;margin-bottom:12px}.symbol-dot{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#0b2028;border:1px solid #2b6974;font-weight:900;color:#fff}.quote-main b{font-size:15px}.quote-main span{display:block;font-size:8px;color:#6d858b;margin-top:3px}.quote-price{margin-left:auto;font:800 20px 'Space Mono'}.quote-change{font:700 10px 'Space Mono';margin-left:8px}
.section-title{font:800 11px 'Space Mono';letter-spacing:.8px;margin:18px 0 9px;color:#dff7ee}.section-title:before{content:"";display:inline-block;width:4px;height:13px;background:var(--green);margin-right:7px;vertical-align:-2px;border-radius:2px}
.metric-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}.metric{padding:12px;border:1px solid #12333b;border-radius:12px;background:#061116;min-height:88px;transition:.2s}.metric:hover{border-color:#2b8c67;transform:translateY(-2px);box-shadow:0 8px 25px #00ff7712}.metric-label{font:700 8px 'Space Mono';color:#70868d}.metric-value{font:800 17px 'Space Mono';margin-top:8px}.metric-sub{font-size:8px;color:#5f747a;margin-top:5px}.structure{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.level{padding:13px;border-radius:12px;background:#061116;border:1px solid #153942}.level.call{border-color:#1c6147}.level.put{border-color:#6b3141}.level.gold{border-color:#6c5b2b}.level-name{font:700 8px 'Space Mono';color:#71878d}.level-price{font:800 18px 'Space Mono';margin-top:8px}
.panel{padding:10px;overflow:hidden}.panel-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:7px}.panel-head b{font-size:11px}.panel-head span{font:8px 'Space Mono';color:#657d83}.two-col{display:grid;grid-template-columns:1.25fr .75fr;gap:10px}.three-col{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:10px}
.news-card-wrap{padding:10px;position:sticky;top:12px;max-height:calc(100vh - 35px);overflow:auto}.news-head{display:flex;justify-content:space-between;align-items:center;padding:5px 2px 9px}.news-head b{font-size:12px}.live{color:#5cff9d;border:1px solid #1b7350;background:#06251b;border-radius:20px;padding:4px 7px;font:700 7px 'Space Mono'}.news-item{padding:11px;border:1px solid #173b43;background:#061116;border-radius:11px;margin:7px 0;transition:.2s}.news-item:hover{border-color:#4aff92;transform:translateX(-2px);box-shadow:0 0 20px #00ff7712}.news-meta{font-size:7px;color:#71878d;display:flex;gap:6px;align-items:center;margin-bottom:6px}.badge{font:700 7px 'Space Mono';border-radius:10px;padding:3px 6px}.badge.high{color:#ff708a;border:1px solid #743144;background:#2a0c16}.badge.medium{color:#f3ca59;border:1px solid #68572a;background:#211b0a}.badge.normal{color:#8ea4aa;border:1px solid #294148;background:#0c161a}.news-link{font-size:10px;line-height:1.45;color:#dcebe8;text-decoration:none}.news-link:hover{color:#5cff9d}.news-empty{padding:18px;text-align:center;color:#637980;font-size:9px;border:1px dashed #1b3b42;border-radius:10px}
.data-note{font:8px 'Space Mono';color:#5e757c;padding:8px 2px}.status{display:inline-flex;align-items:center;gap:5px;font:8px 'Space Mono';color:#5cff9d}.dot{width:6px;height:6px;border-radius:50%;background:#46ff91;box-shadow:0 0 10px #46ff91;animation:pulse 1.6s infinite}@keyframes pulse{50%{opacity:.35;transform:scale(.7)}}
.bottom-nav{display:none}
@media(max-width:1100px){.ticker-strip{display:none}.metric-grid{grid-template-columns:repeat(3,1fr)}.three-col{grid-template-columns:1fr 1fr}.nav-card{display:none}}
@media(max-width:700px){.block-container{padding:7px 8px 70px!important}.tws-header{padding:7px 8px;border-radius:12px;gap:8px}.tws-logo{width:62px;height:48px}.brand{min-width:0}.brand-title{font-size:11px;white-space:nowrap}.brand-sub{font-size:6px;letter-spacing:1px}.search-box{height:39px;font-size:0;padding:0 10px;justify-content:center}.search-icon{font-size:21px}.kbd{display:none}.metric-grid{grid-template-columns:repeat(2,1fr)}.structure{grid-template-columns:repeat(2,1fr)}.two-col,.three-col{grid-template-columns:1fr}.hero{padding:15px}.hero h1{font-size:20px}.hero p{font-size:7px;line-height:1.6}.quote{padding:10px}.quote-price{font-size:15px}.quote-change{font-size:8px}.desktop-news{display:none!important}.mobile-news-btn{display:block!important}.bottom-nav{position:fixed;display:grid;grid-template-columns:repeat(4,1fr);gap:5px;left:7px;right:7px;bottom:7px;padding:6px;background:#031014ee;backdrop-filter:blur(15px);border:1px solid #16414a;border-radius:13px;z-index:9999;box-shadow:0 8px 30px #000}.bottom-nav .stButton>button{font-size:8px!important;padding:7px 2px!important;height:34px!important}.panel{border-radius:12px}.news-dialog-card{padding:10px}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# STATE / SYMBOLS
# ============================================================
POPULAR=["SPY","QQQ","IWM","NVDA","AMD","AAPL","TSLA","MSFT","META","AMZN","GOOGL","NFLX","AVGO","INTC","MU","PLTR","COIN","BTC-USD","ETH-USD","SOL-USD","DOGE-USD","XRP-USD"]
ALIASES={"BTC":"BTC-USD","BITCOIN":"BTC-USD","ETH":"ETH-USD","ETHEREUM":"ETH-USD","SOL":"SOL-USD","SOLANA":"SOL-USD","DOGE":"DOGE-USD","DOGECOIN":"DOGE-USD","XRP":"XRP-USD"}
CRYPTO_NAMES={"BTC-USD":"Bitcoin","ETH-USD":"Ethereum","SOL-USD":"Solana","DOGE-USD":"Dogecoin","XRP-USD":"XRP"}
if "ticker" not in st.session_state: st.session_state.ticker="SPY"
if "view" not in st.session_state: st.session_state.view="Overview"

def norm(s): return ALIASES.get((s or "").strip().upper().replace(" ",""),(s or "").strip().upper().replace(" ",""))
def crypto(s): return s.endswith("-USD")
def esc(x): return html_lib.escape(str(x),quote=True)
def money(x):
    try:
        if pd.isna(x): return "N/A"
        return f"${float(x):,.2f}"
    except: return "N/A"
def large(x):
    try:
        x=float(x)
        if abs(x)>=1e9:return f"${x/1e9:.2f}B"
        if abs(x)>=1e6:return f"${x/1e6:.2f}M"
        if abs(x)>=1e3:return f"${x/1e3:.1f}K"
        return f"${x:,.0f}"
    except:return "N/A"

def age_text(h): return f"{max(1,int(h*60))}m ago" if h<1 else f"{h:.1f}h ago"

# ============================================================
# LIVE PRICE SOURCES
# ============================================================
@st.cache_data(ttl=30,show_spinner=False)
def stock_quote(symbol):
    t=yf.Ticker(symbol)
    try:
        fi=t.fast_info
        p=float(fi.get("lastPrice"))
        prev=float(fi.get("previousClose")) if fi.get("previousClose") else np.nan
        if not np.isfinite(p): raise ValueError
        return {"price":p,"prev":prev,"source":"Yahoo Finance"}
    except Exception:
        h=t.history(period="2d",interval="1d",auto_adjust=False)
        if h.empty: raise ValueError(f"No live quote returned for {symbol}")
        p=float(h["Close"].iloc[-1]); prev=float(h["Close"].iloc[-2]) if len(h)>1 else np.nan
        return {"price":p,"prev":prev,"source":"Yahoo Finance"}

@st.cache_data(ttl=15,show_spinner=False)
def binance_quote(symbol):
    base=symbol.replace("-USD","")
    r=requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={base}USDT",headers={"User-Agent":"Mozilla/5.0"},timeout=8)
    r.raise_for_status(); d=r.json()
    p=float(d["lastPrice"]); pct=float(d["priceChangePercent"])
    return {"price":p,"prev":p/(1+pct/100) if pct>-99 else p,"pct":pct,"source":"Binance spot"}

def live_quote(symbol):
    if crypto(symbol):
        try:return binance_quote(symbol)
        except Exception:
            return stock_quote(symbol)
    return stock_quote(symbol)

# ============================================================
# LIVE NEWS
# ============================================================
HIGH=["fed","fomc","rate decision","interest rate","cpi","inflation","ppi","nfp","payroll","gdp","powell","sec","approval","etf","earnings","guidance","revenue","forecast","downgrade","upgrade","acquisition","merger","bankruptcy","default","tariff","sanction","lawsuit","hack","war","strike","investigation"]
MED=["analyst","outlook","launch","partnership","contract","production","supply","demand","funding","buyback","dividend","target"]

def impact(title):
    s=title.lower()
    if any(k in s for k in HIGH):return "HIGH","high"
    if any(k in s for k in MED):return "MEDIUM","medium"
    return "NORMAL","normal"

def item(title,pub,link,ts):
    now=time.time()
    try: ts=float(ts)
    except: ts=now
    if ts>now+3600:ts=now
    age=max(0,(now-ts)/3600); level,cls=impact(title)
    return {"title":title.strip(),"publisher":pub or "Market News","link":link or "#","age":age,"impact":level,"cls":cls}

@st.cache_data(ttl=180,show_spinner=False)
def news_google(symbol):
    base=symbol.replace("-USD",""); name=CRYPTO_NAMES.get(symbol,"")
    q=f"{base} {name} market" if name else f"{base} stock"
    url=f"https://news.google.com/rss/search?q={quote_plus(q)}&hl=en-US&gl=US&ceid=US:en"
    try:
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=10); r.raise_for_status()
        root=ET.fromstring(r.content); out=[]
        for x in root.findall(".//item"):
            title=x.findtext("title") or ""; link=x.findtext("link") or "#"; pub=x.findtext("source") or "Google News"; dt=x.findtext("pubDate")
            try:ts=pd.Timestamp(dt).timestamp()
            except:ts=time.time()
            out.append(item(title,pub,link,ts))
        return out
    except:return []

@st.cache_data(ttl=180,show_spinner=False)
def news_yahoo(symbol):
    try:
        url=f"https://query1.finance.yahoo.com/v1/finance/search?q={quote_plus(symbol.replace('-USD',''))}&newsCount=30&quotesCount=0"
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=10); r.raise_for_status(); d=r.json(); out=[]
        for x in d.get("news",[]):
            title=x.get("title") or ""; link=x.get("link") or "#"; pub=x.get("publisher") or "Yahoo Finance"; ts=x.get("providerPublishTime",time.time())
            if title:out.append(item(title,pub,link,ts))
        return out
    except:return []

@st.cache_data(ttl=180,show_spinner=False)
def news_yf(symbol):
    try: raw=yf.Ticker(symbol).news or []
    except:return []
    out=[]
    for x in raw:
        c=x.get("content",x); title=c.get("title") or x.get("title")
        if not title:continue
        ts=c.get("providerPublishTime") or x.get("providerPublishTime")
        if not ts:
            try:ts=pd.Timestamp(c.get("pubDate") or x.get("pubDate")).timestamp()
            except:ts=time.time()
        p=c.get("provider",{}); pub=p.get("displayName") if isinstance(p,dict) else None
        cu=c.get("canonicalUrl") or c.get("clickThroughUrl"); link=cu.get("url") if isinstance(cu,dict) else None
        out.append(item(title,pub or x.get("publisher") or "Market News",link or x.get("link") or "#",ts))
    return out

@st.cache_data(ttl=180,show_spinner=False)
def load_news(symbol):
    rows=news_google(symbol)+news_yahoo(symbol)+news_yf(symbol); seen=set(); out=[]
    for n in rows:
        if n["age"]>24:continue
        k=re.sub(r"[^a-z0-9]","",n["title"].lower())[:160]
        if k in seen:continue
        seen.add(k);out.append(n)
    rank={"HIGH":0,"MEDIUM":1,"NORMAL":2};out.sort(key=lambda x:(rank[x["impact"]],x["age"]))
    return out[:15]

def render_news(items,compact=False):
    if not items:
        st.markdown('<div class="news-empty">No live headlines returned for this symbol. Press Refresh or try another market.</div>',unsafe_allow_html=True);return
    for n in items:
        st.markdown(f'''<div class="news-item"><div class="news-meta"><span class="badge {n['cls']}">{n['impact']}</span><span>{esc(n['publisher'])}</span><span>·</span><span>{age_text(n['age'])}</span></div><a class="news-link" href="{esc(n['link'])}" target="_blank" rel="noopener">{esc(n['title'])}</a></div>''',unsafe_allow_html=True)

# ============================================================
# OPTIONS — STOCKS VIA YAHOO; BTC/ETH VIA DERIBIT PUBLIC API
# ============================================================
def clean_chain(df,side,exp):
    if df is None or df.empty:return pd.DataFrame()
    x=df.copy(); x["side"]=side;x["expiration"]=exp
    for c in ["strike","openInterest","volume","impliedVolatility"]:x[c]=pd.to_numeric(x.get(c),errors="coerce")
    x["openInterest"]=x["openInterest"].fillna(0);x["volume"]=x["volume"].fillna(0);x["impliedVolatility"]=x["impliedVolatility"].fillna(0)
    return x.dropna(subset=["strike"])

@st.cache_data(ttl=120,show_spinner=False)
def yahoo_options(symbol,n_exp=6):
    t=yf.Ticker(symbol); q=stock_quote(symbol); ex=list(t.options)
    if not ex:raise ValueError("No Yahoo option expirations available for this symbol")
    rows=[]
    for e in ex[:n_exp]:
        try:
            oc=t.option_chain(e);rows.extend([clean_chain(oc.calls,"CALL",e),clean_chain(oc.puts,"PUT",e)])
        except:continue
    opt=pd.concat([x for x in rows if not x.empty],ignore_index=True)
    return q,opt,ex[:n_exp]

@st.cache_data(ttl=30,show_spinner=False)
def deribit_options(symbol):
    base=symbol.replace("-USD","").upper()
    if base not in ("BTC","ETH"):raise ValueError("Deribit public options are available here for BTC and ETH")
    inst=requests.get(f"https://www.deribit.com/api/v2/public/get_instruments?currency={base}&kind=option&expired=false",timeout=10).json()["result"]
    q=requests.get(f"https://www.deribit.com/api/v2/public/ticker?instrument_name={base}-PERPETUAL",timeout=10).json()["result"]
    spot=float(q["last_price"]); now=datetime.now(timezone.utc).timestamp()*1000
    rows=[]
    for ins in inst:
        try:
            name=ins["instrument_name"]; parts=name.split("-"); exp=int(parts[1]); strike=float(parts[2]); cp=parts[3]
            if exp<now:continue
            tkr=requests.get(f"https://www.deribit.com/api/v2/public/ticker?instrument_name={name}",timeout=5).json()["result"]
            oi=float(tkr.get("open_interest") or 0); iv=float(tkr.get("mark_iv") or 0)/100
            rows.append({"strike":strike,"openInterest":oi,"volume":float(tkr.get("stats",{}).get("volume") or 0),"impliedVolatility":iv,"side":"CALL" if cp=="C" else "PUT","expiration":datetime.fromtimestamp(exp/1000,timezone.utc).strftime("%Y-%m-%d")})
        except:continue
    return {"price":spot,"prev":spot},pd.DataFrame(rows)

def max_pain(ch):
    strikes=np.sort(ch.strike.unique())
    if not len(strikes):return np.nan
    c=ch[ch.side=="CALL"];p=ch[ch.side=="PUT"]
    ck,co=c.strike.values,c.openInterest.values;pk,po=p.strike.values,p.openInterest.values
    vals=[np.sum(np.maximum(k-ck,0)*co)+np.sum(np.maximum(pk-k,0)*po) for k in strikes]
    return float(strikes[int(np.argmin(vals))])

def bs_gamma(S,K,T,sigma):
    if sigma<=0 or T<=0:return 0.0
    d1=(math.log(S/K)+0.5*sigma*sigma*T)/(sigma*math.sqrt(T));return math.exp(-.5*d1*d1)/(math.sqrt(2*math.pi)*S*sigma*math.sqrt(T))

def analyze_options(opt,spot):
    if opt.empty:raise ValueError("Empty option chain")
    exp_rows=[];gex_rows=[]
    for exp,ch in opt.groupby("expiration"):
        try:dte=max((pd.Timestamp(exp).tz_localize("UTC")-pd.Timestamp.now(tz="UTC")).total_seconds()/86400,0.01)
        except:dte=.01
        atm=ch.loc[(ch.strike-spot).abs().idxmin(),"impliedVolatility"]*100 if not ch.empty else np.nan
        pc=ch.loc[ch.side=="PUT","openInterest"].sum()/max(ch.loc[ch.side=="CALL","openInterest"].sum(),1)
        exp_rows.append([exp,round(dte,1),max_pain(ch),atm,pc,int(ch.openInterest.sum()),int(ch.volume.sum())])
        for _,r in ch.iterrows():
            T=dte/365; g=bs_gamma(spot,float(r.strike),T,float(r.impliedVolatility)); sign=1 if r.side=="CALL" else -1
            gex_rows.append([float(r.strike),sign*g*float(r.openInterest)*100*spot*spot*.01])
    ex=pd.DataFrame(exp_rows,columns=["Expiration","DTE","Max Pain","ATM IV %","Put/Call OI","Total OI","Volume"])
    g=pd.DataFrame(gex_rows,columns=["strike","GEX"])
    calls=opt[opt.side=="CALL"];puts=opt[opt.side=="PUT"]
    call_wall=float(calls[calls.strike>=spot].groupby("strike").openInterest.sum().idxmax()) if not calls[calls.strike>=spot].empty else np.nan
    put_wall=float(puts[puts.strike<=spot].groupby("strike").openInterest.sum().idxmax()) if not puts[puts.strike<=spot].empty else np.nan
    profile=[]
    grid=np.linspace(spot*.85,spot*1.15,90)
    for S in grid:
        total=0
        for _,r in opt.iterrows():
            T=max((pd.Timestamp(r.expiration)-pd.Timestamp.now()).total_seconds()/86400/365,.003)
            total+=bs_gamma(S,float(r.strike),T,float(r.impliedVolatility))*float(r.openInterest)*100*S*S*.01*(1 if r.side=="CALL" else -1)
        profile.append(total)
    flip=np.nan
    if len(g):
        by=g.groupby("strike").GEX.sum().sort_index();
        vals=by.values;ks=by.index.values
        for i in range(1,len(vals)):
            if vals[i-1]*vals[i]<0:flip=float((ks[i-1]+ks[i])/2);break
    return ex,g,grid,np.array(profile),call_wall,put_wall,flip

# ============================================================
# TOP HEADER + SEARCH
# ============================================================
ticker=st.session_state.ticker
try:q=live_quote(ticker)
except Exception as e:q={"price":np.nan,"prev":np.nan,"source":"No live quote"}
pct=(q["price"]/q["prev"]-1)*100 if np.isfinite(q.get("prev",np.nan)) and q.get("prev") else np.nan

st.markdown(f'''<div class="tws-header"><img class="tws-logo" src="data:image/jpeg;base64,{LOGO_B64}"><div class="brand"><div class="brand-title">T.W.S <span>GAMMA TERMINAL</span></div><div class="brand-sub">TRADE WITH SOHAIB · LIVE MARKET INTELLIGENCE</div></div><div class="search-box"><span class="search-icon">⌕</span><span>Search stock, ETF or crypto…</span><span class="kbd">CTRL + K</span></div><div class="ticker-strip"><div class="ticker"><b>BTC</b><span class="up">LIVE</span></div><div class="ticker"><b>ETH</b><span class="up">LIVE</span></div><div class="ticker"><b>{esc(ticker.replace('-USD',''))}</b><span class="up">SELECTED</span></div></div></div>''',unsafe_allow_html=True)

c1,c2,c3,c4=st.columns([1,1,1.2,5],vertical_alignment="center")
with c1:
    with st.popover("⌕  SEARCH",use_container_width=True):
        sv=st.text_input("Symbol",value=ticker,placeholder="NVDA / AAPL / SPY / BTC / ETH",key="search_symbol")
        quick=st.selectbox("Quick markets",POPULAR,index=POPULAR.index(ticker) if ticker in POPULAR else 0)
        x,y=st.columns(2)
        if x.button("APPLY",use_container_width=True):
            s=norm(sv)
            if s:st.session_state.ticker=s;st.cache_data.clear();st.rerun()
        if y.button("QUICK",use_container_width=True):
            st.session_state.ticker=norm(quick);st.cache_data.clear();st.rerun()
with c2:
    if st.button("NEWS",use_container_width=True):
        show_news_dialog()
with c3:
    if st.button("↻ REFRESH",use_container_width=True):st.cache_data.clear();st.rerun()
with c4:
    st.markdown(f'<div class="status"><span class="dot"></span> LIVE DATA · {esc(q["source"])} · {esc(ticker)}</div>',unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
news=load_news(ticker)

@st.dialog(f"{ticker} · LIVE NEWS", width="large")
def show_news_dialog():
    st.caption("Live symbol-linked headlines · last 24 hours")
    render_news(news)

opt=None;exp_table=None;g_opt=None;profile_grid=None;profile=None;call_wall=put_wall=gamma_flip=mp_main=atm_iv=net_gex=np.nan;magnetic=np.nan
options_error=None
try:
    if crypto(ticker):
        qq,opt=deribit_options(ticker)
        q.update(qq)
    else:
        qq,opt,_=yahoo_options(ticker,6)
        q.update(qq)
    exp_table,g_opt,profile_grid,profile,call_wall,put_wall,gamma_flip=analyze_options(opt,float(q["price"]))
    valid=exp_table.dropna(subset=["Max Pain"]);mp_main=float(valid.iloc[0]["Max Pain"]) if not valid.empty else np.nan
    iv=exp_table["ATM IV %"].dropna();atm_iv=float(iv.iloc[0]) if not iv.empty else np.nan
    levels=[x for x in [call_wall,put_wall,gamma_flip,mp_main] if pd.notna(x)];magnetic=min(levels,key=lambda x:abs(x-q["price"])) if levels else np.nan
    net_gex=float(g_opt.GEX.sum()) if g_opt is not None else np.nan
except Exception as e:
    options_error=str(e)

# ============================================================
# NAV / VIEW SELECTION
# ============================================================
nav,main,right=st.columns([.82,3.55,1.25],gap="medium")
with nav:
    st.markdown(f'''<div class="nav-card"><img class="nav-logo" src="data:image/jpeg;base64,{LOGO_B64}"><div class="nav-section">ANALYSIS</div>''',unsafe_allow_html=True)
    for label in ["Overview","Gamma Exposure","Options Flow","Technical Analysis","Options Chain","News"]:
        if st.button(label,use_container_width=True,key="nav_"+label):st.session_state.view=label;st.rerun()
    st.markdown('<div class="nav-section">MARKETS</div>',unsafe_allow_html=True)
    for label in ["Stocks","Crypto"]:
        if st.button(label,use_container_width=True,key="m_"+label):
            if label=="Crypto":st.session_state.ticker="BTC-USD"
            else:st.session_state.ticker="SPY"
            st.session_state.view="Overview";st.cache_data.clear();st.rerun()
    st.markdown(f'<div style="margin-top:15px;padding:10px;border-top:1px solid #12333b;font-size:8px;color:#637980">SELECTED<br><b style="color:#dceee8;font-size:12px">{esc(ticker)}</b><br><br><span class="status"><span class="dot"></span> LIVE</span></div></div>',unsafe_allow_html=True)

with right:
    st.markdown('<div class="desktop-news">',unsafe_allow_html=True)
    st.markdown('<div class="news-card-wrap"><div class="news-head"><b>NEWS & EVENTS</b><span class="live">LIVE</span></div>',unsafe_allow_html=True)
    render_news(news,True)
    st.markdown('</div></div>',unsafe_allow_html=True)

with main:
    st.markdown(f'''<div class="quote"><div class="symbol-dot">{esc(ticker.replace('-USD','')[:5])}</div><div class="quote-main"><b>{esc(ticker)}</b><span>{'Crypto · Deribit/Binance live' if crypto(ticker) else 'Equity/ETF · Yahoo Finance live'}</span></div><div class="quote-price">{money(q['price'])}</div><div class="quote-change {'up' if pct>=0 else 'down'}">{('+' if pct>=0 else '')}{pct:.2f}%</div></div>''',unsafe_allow_html=True)
    st.markdown('''<div class="hero"><span class="live-pill">● LIVE MARKET INTELLIGENCE</span><h1>T.W.S GAMMA TERMINAL</h1><p>TRADE WITH SOHAIB · OPTIONS FLOW · GAMMA EXPOSURE · TECHNICAL ANALYSIS · LIVE NEWS</p></div>''',unsafe_allow_html=True)

    # Mobile news popup
    if st.button("OPEN LIVE NEWS",use_container_width=True,key="mobile_news_open"):
        show_news_dialog()

    if st.session_state.view=="News":
        st.markdown('<div class="section-title">LIVE NEWS INTELLIGENCE</div>',unsafe_allow_html=True)
        render_news(news)
    elif st.session_state.view=="Technical Analysis":
        st.markdown('<div class="section-title">TECHNICAL ANALYSIS · LIVE MARKET DATA</div>',unsafe_allow_html=True)
        try:
            if crypto(ticker):
                base=ticker.replace("-USD","");u=f"https://api.binance.com/api/v3/klines?symbol={base}USDT&interval=1h&limit=120";d=requests.get(u,timeout=10).json();h=pd.DataFrame(d,columns=["t","o","h","l","c","v","x1","x2","x3","x4","x5","x6"]);h["date"]=pd.to_datetime(h.t,unit="ms");h["price"]=pd.to_numeric(h.c);h["ma20"]=h.price.rolling(20).mean()
            else:
                h=yf.Ticker(ticker).history(period="3mo",interval="1d",auto_adjust=False).reset_index();h["date"]=pd.to_datetime(h.iloc[:,0]);h["price"]=h.Close.astype(float);h["ma20"]=h.price.rolling(20).mean()
            h=h.dropna(subset=["price"])
            ch=alt.Chart(h).mark_line(color="#46ff91",size=2.5).encode(x="date:T",y=alt.Y("price:Q",scale=alt.Scale(zero=False)),tooltip=["date","price"])
            ma=alt.Chart(h.dropna()).mark_line(color="#f2c85b",size=1.5).encode(x="date:T",y="ma20:Q")
            st.altair_chart((ch+ma).properties(height=430),use_container_width=True)
            last=float(h.price.iloc[-1]);ma20=float(h.ma20.iloc[-1]);trend="BULLISH" if last>ma20 else "BEARISH"
            a,b,c=st.columns(3);a.metric("LIVE PRICE",money(last));b.metric("20-PERIOD MA",money(ma20));c.metric("TREND",trend)
        except Exception as e:st.error(f"Technical data unavailable: {e}")
    elif st.session_state.view=="Options Flow":
        if options_error:st.error(f"Live options data unavailable: {options_error}")
        else:
            st.markdown('<div class="section-title">OPTIONS FLOW · LIVE OPEN INTEREST</div>',unsafe_allow_html=True)
            flow=opt.groupby("side")["openInterest"].sum().reset_index();st.dataframe(flow,use_container_width=True,hide_index=True)
            oi=opt.groupby(["strike","side"]).openInterest.sum().reset_index();lo=q["price"]*.85;hi=q["price"]*1.15
            oi=oi[(oi.strike>=lo)&(oi.strike<=hi)]
            chart=alt.Chart(oi).mark_bar().encode(x=alt.X("strike:Q"),y=alt.Y("openInterest:Q"),color=alt.Color("side:N",scale=alt.Scale(domain=["CALL","PUT"],range=["#46ff91","#ff4e70"])),tooltip=["strike","side","openInterest"])
            st.altair_chart(chart.properties(height=430),use_container_width=True)
    elif st.session_state.view=="Options Chain":
        if options_error:st.error(f"Live options data unavailable: {options_error}")
        else:
            st.markdown('<div class="section-title">LIVE OPTION CHAIN</div>',unsafe_allow_html=True)
            near=opt.iloc[(opt.strike-q["price"]).abs().argsort()[:24]].sort_values(["strike","side"])
            show=near[["expiration","strike","side","impliedVolatility","openInterest","volume"]].copy();show["impliedVolatility"]=(show["impliedVolatility"]*100).round(2)
            st.dataframe(show,use_container_width=True,hide_index=True,height=560)
    else:
        # Overview / Gamma Exposure
        st.markdown('<div class="section-title">LIVE OPTIONS SNAPSHOT</div>',unsafe_allow_html=True)
        vals=[("SPOT PRICE",money(q["price"]),"Live underlying"),("CALL WALL",money(call_wall),"Highest call OI above spot"),("PUT WALL",money(put_wall),"Highest put OI below spot"),("GAMMA FLIP",money(gamma_flip),"Estimated zero-cross"),("MAX PAIN",money(mp_main),"Nearest expiration"),("ATM IV",f"{atm_iv:.2f}%" if pd.notna(atm_iv) else "N/A","Nearest expiration")]
        st.markdown('<div class="metric-grid">'+''.join([f'<div class="metric"><div class="metric-label">{a}</div><div class="metric-value">{b}</div><div class="metric-sub">{c}</div></div>' for a,b,c in vals])+'</div>',unsafe_allow_html=True)
        st.markdown('<div class="section-title">KEY MARKET STRUCTURE</div>',unsafe_allow_html=True)
        cd=(call_wall/q["price"]-1)*100 if pd.notna(call_wall) else np.nan;pdst=(put_wall/q["price"]-1)*100 if pd.notna(put_wall) else np.nan
        st.markdown(f'''<div class="structure"><div class="level gold"><div class="level-name">MAGNETIC LEVEL</div><div class="level-price">{money(magnetic)}</div></div><div class="level call"><div class="level-name">CALL WALL DISTANCE</div><div class="level-price up">{cd:+.2f}%</div></div><div class="level put"><div class="level-name">PUT WALL DISTANCE</div><div class="level-price down">{pdst:+.2f}%</div></div><div class="level gold"><div class="level-name">NET GEX / 1% MOVE</div><div class="level-price">{large(net_gex)}</div></div></div>''',unsafe_allow_html=True)
        if options_error:
            st.warning(f"Options/Gamma data is not available for {ticker}: {options_error}. Live price and news remain available.")
        else:
            st.markdown('<div class="section-title">GAMMA EXPOSURE · LIVE ESTIMATE</div>',unsafe_allow_html=True)
            lo=q["price"]*.85;hi=q["price"]*1.15;gs=g_opt.groupby("strike").GEX.sum().reset_index();gs=gs[(gs.strike>=lo)&(gs.strike<=hi)];gs["M"] = gs.GEX/1e6;gs["dir"]=np.where(gs.M>=0,"Positive","Negative")
            chart=alt.Chart(gs).mark_bar().encode(x=alt.X("strike:Q",scale=alt.Scale(domain=[lo,hi])),y=alt.Y("M:Q",title="GEX $M / 1%"),color=alt.Color("dir:N",scale=alt.Scale(domain=["Positive","Negative"],range=["#46ff91","#ff4e70"]),legend=None),tooltip=["strike",alt.Tooltip("M:Q",format=",.2f")])
            st.altair_chart(chart.properties(height=390),use_container_width=True)
            a,b=st.columns(2)
            with a:
                st.markdown('<div class="panel"><div class="panel-head"><b>GEX PROFILE VS SPOT</b><span>LIVE MODEL</span></div>',unsafe_allow_html=True)
                prof=pd.DataFrame({"price":profile_grid,"gex":profile/1e6});pc=alt.Chart(prof).mark_line(color="#46ff91",size=2.5).encode(x="price:Q",y=alt.Y("gex:Q",title="GEX $M"));st.altair_chart(pc.properties(height=300),use_container_width=True);st.markdown('</div>',unsafe_allow_html=True)
            with b:
                st.markdown('<div class="panel"><div class="panel-head"><b>OPEN INTEREST</b><span>LIVE CHAIN</span></div>',unsafe_allow_html=True)
                oi=opt.groupby(["strike","side"]).openInterest.sum().reset_index();oi=oi[(oi.strike>=lo)&(oi.strike<=hi)];oc=alt.Chart(oi).mark_bar().encode(x=alt.X("strike:Q"),y="openInterest:Q",color=alt.Color("side:N",scale=alt.Scale(domain=["CALL","PUT"],range=["#46ff91","#ff4e70"])),tooltip=["strike","side","openInterest"]);st.altair_chart(oc.properties(height=300),use_container_width=True);st.markdown('</div>',unsafe_allow_html=True)

    # Always-visible compact live data below selected module
    if st.session_state.view=="Overview":
        st.markdown('<div class="section-title">EXPIRATION DATA · LIVE</div>',unsafe_allow_html=True)
        if exp_table is not None:st.dataframe(exp_table,use_container_width=True,hide_index=True)
        st.markdown('<div class="section-title">TECHNICAL ANALYSIS · LIVE</div>',unsafe_allow_html=True)
        try:
            if crypto(ticker):
                base=ticker.replace("-USD","");d=requests.get(f"https://api.binance.com/api/v3/klines?symbol={base}USDT&interval=1h&limit=72",timeout=8).json();h=pd.DataFrame(d,columns=["t","o","h","l","c","v","a","b","c2","d","e","f"]);h["date"]=pd.to_datetime(h.t,unit="ms");h["price"]=pd.to_numeric(h.c)
            else:
                h=yf.Ticker(ticker).history(period="1mo",interval="1d",auto_adjust=False).reset_index();h["date"]=pd.to_datetime(h.iloc[:,0]);h["price"]=h.Close.astype(float)
            h["ma"]=h.price.rolling(10).mean();hc=alt.Chart(h).mark_line(color="#53dfff",size=2).encode(x="date:T",y=alt.Y("price:Q",scale=alt.Scale(zero=False)),tooltip=["date","price"]);hm=alt.Chart(h.dropna()).mark_line(color="#f2c85b",size=1.5).encode(x="date:T",y="ma:Q");st.altair_chart((hc+hm).properties(height=310),use_container_width=True)
        except Exception as e:st.info(f"Technical chart unavailable: {e}")

# ============================================================
# MOBILE BOTTOM NAV
# ============================================================
st.markdown('<div class="bottom-nav">',unsafe_allow_html=True)
mb1,mb2,mb3,mb4=st.columns(4)
for col,label in zip([mb1,mb2,mb3,mb4],["HOME","GAMMA","TECH","NEWS"]):
    with col:
        if st.button(label,use_container_width=True,key="bottom_"+label):
            st.session_state.view={"HOME":"Overview","GAMMA":"Gamma Exposure","TECH":"Technical Analysis","NEWS":"News"}[label];st.rerun()
st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="data-note">T.W.S · TRADE WITH SOHAIB · LIVE PUBLIC MARKET DATA · OPTIONS/GEX ARE MODELS FROM PUBLIC MARKET DATA · NOT FINANCIAL ADVICE</div>',unsafe_allow_html=True)
