import streamlit as st
import requests
import json
import urllib.parse
import re

# ==========================================
# 1. الإعدادات الأساسية (Foundation Locked)
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | The Empire", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري في الخزنة.")
    st.stop()

# ==========================================
# 2. محركات الذكاء الاصطناعي 
# ==========================================
@st.cache_data(ttl=3600)
def get_best_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models = res.json().get('models', [])
            valid_models = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', []) and 'vision' not in m['name'] and 'aqa' not in m['name'] and 'embedding' not in m['name'] and 'audio' not in m['name']]
            valid_models.sort(key=lambda x: (0 if '2.5-flash' in x else 1 if '2.0-flash' in x else 2 if '1.5-flash' in x else 3, x))
            return valid_models
        return []
    except: return []

def call_gemini_direct(prompt):
    models = get_best_models()
    if not models: return "Error: No valid models found."
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        try:
            res = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
            if res.status_code == 200: return res.json()['candidates'][0]['content']['parts'][0]['text']
        except: continue
    return "Error: Request failed."

def fetch_live_trends(niche, platform):
    prompt = f"""
    Act as an e-commerce data extractor. Find 3 highly trending products in the '{niche}' niche on {platform}.
    Return ONLY a valid JSON array.
    [
      {{"name": "Precise Product Name", "price": "$XX.XX", "score": "97", "category": "CATEGORY", "specs": "Short physical description"}}
    ]
    IMPORTANT: "specs" MUST be a very precise physical description.
    """
    response = call_gemini_direct(prompt)
    if "Error:" in response: return None
    try:
        clean_json = response.replace('```json', '').replace('```', '').strip()
        match = re.search(r'\[.*\]', clean_json, re.DOTALL)
        return json.loads(match.group(0)) if match else json.loads(clean_json)
    except: return None

MARKET_LOGOS = {
    "Amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
    "TikTok Shop": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg",
    "AliExpress": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Aliexpress_logo.svg"
}

# ==========================================
# 3. التصميم الإمبراطوري المتطور 
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Montserrat:wght@200;300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Montserrat', sans-serif; }
#MainMenu, footer, header, [data-testid="stDecoration"] { display: none !important; }

/* 🛡️ إخفاء السهم وتجميل شريط التمرير */
[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] { display: none !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #d4af37; }

/* الشريط الجانبي واللوجو */
[data-testid="stSidebar"] { background-color: #080808 !important; border-right: 1px solid #1a1a1a; padding-top: 20px;}
[data-testid="stSidebarNav"] { display: none; }
.imperial-logo-box { text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(212, 175, 55, 0.15); margin-bottom: 20px; }
.imperial-logo-wrapper { display: flex; justify-content: center; align-items: baseline; gap: 8px; }
.imperial-logo { font-family: 'Cinzel', serif; font-size: 2.2rem; font-weight: 700; letter-spacing: 3px; background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase;}
.imperial-ai { font-family: 'Cinzel', serif; font-size: 1.6rem; color: #fff; font-weight: 300; letter-spacing: 2px;}
.imperial-sub { font-family: 'Montserrat', sans-serif; font-size: 0.65rem; color: #666; letter-spacing: 4px; text-transform: uppercase; margin-top: 5px; font-weight: 300;}

div[data-testid="stSidebar"] div.stButton > button { background-color: transparent !important; color: #888 !important; font-family: 'Montserrat', sans-serif; font-weight: 400; font-size: 1rem; border: none; border-radius: 4px; padding: 10px 15px; text-align: left !important; justify-content: flex-start !important; transition: 0.3s; width: 100%; margin-bottom: 5px;}
div[data-testid="stSidebar"] div.stButton > button:hover { color: #d4af37 !important; background-color: rgba(212, 175, 55, 0.05) !important; padding-left: 20px !important;}

/* العناوين والعدادات */
.page-title { font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; margin-bottom: 5px; font-weight: 600;}
.page-sub { font-family: 'Montserrat', sans-serif; font-size: 0.85rem; color: #888; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 40px; font-weight: 300;}

.kpi-card { background: linear-gradient(145deg, #0d0d0d, #111111); border: 1px solid #1a1a1a; border-radius: 12px; padding: 30px; text-align: center; position: relative; overflow: hidden; height:100%; transition: all 0.4s ease;}
.kpi-card:hover { border-color: rgba(212, 175, 55, 0.4); box-shadow: 0 10px 30px rgba(212, 175, 55, 0.05); transform: translateY(-3px);}
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(to right, transparent, #d4af37, transparent); }
.kpi-title { font-family: 'Cinzel', serif; font-size: 0.9rem; color: #d4af37; letter-spacing: 2px; margin-bottom: 15px; text-transform: uppercase;}
.kpi-value { font-family: 'Montserrat', sans-serif; font-size: 3rem; font-weight: 200; color: #fff; line-height: 1;}
.kpi-sub { font-size: 0.75rem; color: #555; margin-top: 10px; font-weight: 300; letter-spacing: 1px;}

.main-btn > button { background-color: #c5a059 !important; color: #000 !important; font-weight: 600; font-family: 'Montserrat', sans-serif; border: none; border-radius: 6px; padding: 12px; transition: 0.3s; width: 100%; letter-spacing: 1px;}
.main-btn > button:hover { background-color: #e8c37b !important; transform: translateY(-2px);}

/* 🌍 خريطة النبض التفاعلية (Heatmap CSS) */
.heatmap-box { background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 12px; padding: 30px; margin-top: 30px; }
.heatmap-title { font-family: 'Cinzel', serif; font-size: 1.2rem; color: #fff; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;}
.heatmap-title span { font-family: 'Montserrat', sans-serif; font-size: 0.7rem; color: #20c997; letter-spacing: 2px; }
.chart-container { display: flex; align-items: flex-end; justify-content: space-around; height: 180px; padding-top: 20px;}
.bar-col { display: flex; flex-direction: column; align-items: center; width: 60px; gap: 10px; }
.bar { width: 100%; background: linear-gradient(to top, rgba(212,175,55,0.1), #d4af37); border-radius: 4px 4px 0 0; position: relative; transition: height 1s ease-in-out;}
.bar:hover { filter: brightness(1.3); box-shadow: 0 0 15px rgba(212,175,55,0.4);}
.bar-value { position: absolute; top: -25px; left: 50%; transform: translateX(-50%); color: #fff; font-size: 0.8rem; font-weight: bold; font-family: 'Montserrat', sans-serif;}
.bar-label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 1px; font-family: 'Montserrat', sans-serif;}

/* الأزرار والكروت الخاصة بالمنتجات */
div[data-testid="stDownloadButton"] > button { background-color: #050505 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; font-family: 'Montserrat', sans-serif; font-weight: 600; border-radius: 6px; padding: 10px; transition: 0.3s; width: 100%; margin-top: 10px;}
div[data-testid="stDownloadButton"] > button:hover { background-color: #d4af37 !important; color: #000 !important; }

.product-card { background: #0a0a0a; border: 1px solid #222; border-radius: 12px; padding: 15px; margin-bottom: 15px; transition: 0.3s;}
.product-card:hover { border-color: #333; }
.product-img { width: 100%; height: 250px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; background: #fff;}
.p-name { color: #fff; font-family: 'Cinzel', serif; font-size: 1.2rem; font-weight: 600; margin-bottom: 10px; min-height: 45px;}
.p-price { color: #d4af37; font-size: 1.4rem; font-weight: 300;}

.stTextInput input, .stSelectbox div[data-baseweb="select"] > div { background-color: #111 !important; color: #fff !important; border: 1px solid #333 !important; border-radius: 6px !important; font-family: 'Montserrat', sans-serif;}

.panel-box { background: #0d0d0d; border: 1px solid #222; border-radius: 12px; padding: 25px; margin-bottom: 20px;}
.panel-header { font-family: 'Cinzel', serif; color: #d4af37; font-size: 1.2rem; margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 10px;}

/* تصميم مشغل الفيديو الوهمي */
.video-player { position: relative; text-align: center; margin-top: 15px; border-radius: 8px; overflow: hidden; border: 1px solid #d4af37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);}
.video-player img { width: 100%; filter: brightness(0.7); display: block;}
.video-play-btn { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; color: rgba(212, 175, 55, 0.9); cursor: pointer; transition: 0.3s;}
.video-play-btn:hover { transform: translate(-50%, -50%) scale(1.1); color: #fff;}
.video-time { position: absolute; bottom: 10px; right: 10px; font-size: 0.8rem; background: rgba(0,0,0,0.8); color: #fff; padding: 3px 8px; border-radius: 4px; font-family: 'Montserrat', sans-serif;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. إدارة التنقل 
# ==========================================
if 'current_tab' not in st.session_state: st.session_state.current_tab = 'dashboard'
if 'radar_step' not in st.session_state: st.session_state.radar_step = 'select_platform'

# ==========================================
# 5. الشريط الجانبي الإمبراطوري 
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="imperial-logo-box">
        <div class="imperial-logo-wrapper">
            <span class="imperial-logo">WAFEEQ</span>
            <span class="imperial-ai">AI</span>
        </div>
        <div class="imperial-sub">From Trend to Brand</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔔 جرس التنبيهات الاستباقية (Ghost Alerts)
    with st.expander("🔔 GHOST ALERTS (2)", expanded=False):
        st.markdown("<div style='font-size:0.8rem; color:#fff; border-left:2px solid #d4af37; padding-left:10px; margin-bottom:10px; font-family:Montserrat;'>🔥 <b>Surge Detected:</b> 40% spike in Luxury Watches on TikTok Gulf!</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.8rem; color:#fff; border-left:2px solid #20c997; padding-left:10px; font-family:Montserrat;'>💡 <b>Market Gap:</b> Competitor 'LuxeTech' just went out of stock. Move now!</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='color:#555; font-size:0.65rem; letter-spacing:2px; margin:20px 0 10px 0; padding-left:5px;'>COMMAND CENTER</div>", unsafe_allow_html=True)
    if st.button("📊 Dashboard", use_container_width=True): st.session_state.current_tab = 'dashboard'
    
    st.markdown("<div style='color:#555; font-size:0.65rem; letter-spacing:2px; margin:20px 0 10px 0; padding-left:5px;'>THE 7 PILLARS</div>", unsafe_allow_html=True)
    if st.button("📡 Omni-Pulse Radar", use_container_width=True): st.session_state.current_tab = 'radar'
    if st.button("🛡️ Trust Shield", use_container_width=True): st.session_state.current_tab = 'shield'
    if st.button("🎧 Concierge", use_container_width=True): st.session_state.current_tab = 'concierge'
    if st.button("📈 Growth Engine", use_container_width=True): st.session_state.current_tab = 'growth'

# ==========================================
# 6. المحتوى الرئيسي 
# ==========================================

if st.session_state.current_tab == 'dashboard':
    st.markdown('<div class="page-title">Command Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Global E-Commerce Overview · Live Operations</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="kpi-card"><div class="kpi-title">Daily Net Profit</div><div class="kpi-value">$14,250</div><div class="kpi-sub">▲ 12.5% VS YESTERDAY</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi-card"><div class="kpi-title">Store Trust Score</div><div class="kpi-value">98.5<span style="font-size:1.5rem;">%</span></div><div class="kpi-sub">BASED ON AI SENTIMENT ANALYSIS</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-card"><div class="kpi-title">Disputes Blocked</div><div class="kpi-value">24</div><div class="kpi-sub">🛡️ $3,120 SAVED TODAY</div></div>', unsafe_allow_html=True)
        
    st.markdown("""
    <div class="heatmap-box">
        <div class="heatmap-title">Global Market Demand Pulse <span>● LIVE SYNC</span></div>
        <div class="chart-container">
            <div class="bar-col"><div class="bar" style="height: 85%;"><div class="bar-value">85%</div></div><div class="bar-label">TikTok</div></div>
            <div class="bar-col"><div class="bar" style="height: 60%;"><div class="bar-value">60%</div></div><div class="bar-label">Amazon</div></div>
            <div class="bar-col"><div class="bar" style="height: 92%;"><div class="bar-value">92%</div></div><div class="bar-label">AliExpress</div></div>
            <div class="bar-col"><div class="bar" style="height: 45%;"><div class="bar-value">45%</div></div><div class="bar-label">Etsy</div></div>
            <div class="bar-col"><div class="bar" style="height: 70%;"><div class="bar-value">70%</div></div><div class="bar-label">eBay</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_tab == 'radar':
    if st.session_state.radar_step == 'select_platform':
        st.markdown('<div class="page-title">Omni-Pulse Radar</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Select a marketplace to hunt trending products</div>', unsafe_allow_html=True)
        
        niche = st.text_input("", placeholder="Enter a niche (e.g. Home Decor, Tech)...", label_visibility="collapsed")
        st.write("")
        
        platforms = ["Amazon", "AliExpress", "TikTok Shop"]
        cols = st.columns(3)
        for i, p in enumerate(platforms):
            with cols[i]:
                logo_url = MARKET_LOGOS.get(p, "")
                st.markdown(f"""
                <div style="background:#111; border:1px solid #222; border-radius:12px; padding:30px; text-align:center; cursor:pointer;">
                    <img src="{logo_url}" style="height:40px; filter:brightness(0) invert(1); opacity:0.8; margin-bottom:20px;">
                    <div style="font-family:'Cinzel', serif; font-size:1.2rem; color:#fff;">{p}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
                if st.button(f"Scan {p}", key=f"scan_{p}"):
                    st.session_state.platform = p
                    st.session_state.niche = niche if niche else "Luxury Goods"
                    st.session_state.radar_step = 'results'
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.radar_step == 'results':
        logo_url = MARKET_LOGOS.get(st.session_state.platform, "")
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:20px; margin-bottom:10px;">
            <img src="{logo_url}" style="height:35px; filter:brightness(0) invert(1);">
            <div class="page-title" style="margin:0;">Trending Analysis</div>
        </div>
        <div class="page-sub">MARKET: {st.session_state.niche.upper()}</div>
        """, unsafe_allow_html=True)
        
        if st.button("← New Scan"):
            st.session_state.radar_step = 'select_platform'
            st.rerun()
            
        with st.spinner("📡 Intercepting live market data..."):
            if 'live_data' not in st.session_state or st.session_state.get('last_niche') != f"{st.session_state.niche}_{st.session_state.platform}":
                st.session_state.live_data = fetch_live_trends(st.session_state.niche, st.session_state.platform)
                st.session_state.last_niche = f"{st.session_state.niche}_{st.session_state.platform}"

        if not st.session_state.live_data:
            st.error("⚠️ AI is busy. Please try another niche.")
        else:
            cols = st.columns(3)
            for i, item in enumerate(st.session_state.live_data):
                with cols[i % 3]:
                    specs = item.get('specs', item.get('name'))
                    safe_prompt = urllib.parse.quote_plus(f"realistic e-commerce product photography of {specs}, isolated on pure white background, highly detailed, 4k")
                    img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=600&height=600&nologo=true&seed={i+300}"
                    
                    st.markdown(f"""
                    <div class="product-card">
                        <img src="{img_url}" class="product-img">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <span style="color:#666; font-size:0.7rem; text-transform:uppercase;">{item.get('category', 'TRENDING')}</span>
                            <span style="border:1px solid #333; color:#d4af37; padding:2px 8px; border-radius:12px; font-size:0.7rem;">↗ {item.get('score', '95')}</span>
                        </div>
                        <div class="p-name">{item.get('name', 'Luxury Product')}</div>
                        <div class="p-price">{item.get('price', '$99.00')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("🔍 Market Gap", key=f"gap_{i}"):
                            st.session_state[f"show_gap_{i}"] = not st.session_state.get(f"show_gap_{i}", False)
                            st.session_state[f"show_profit_{i}"] = False
                    with col_btn2:
                        if st.button("⚖️ What-If Profit", key=f"profit_{i}"):
                            st.session_state[f"show_profit_{i}"] = not st.session_state.get(f"show_profit_{i}", False)
                            st.session_state[f"show_gap_{i}"] = False

                    if st.session_state.get(f"show_gap_{i}"):
                        if f"gap_data_{i}" not in st.session_state:
                            with st.spinner("Analyzing..."):
                                st.session_state[f"gap_data_{i}"] = call_gemini_direct(f"Identify ONE major customer complaint for '{item.get('name')}' and state how to fix it to beat competitors. 2 sentences max.")
                        st.info(f"💡 **Market Gap:** {st.session_state[f'gap_data_{i}']}")

                    # 🎛️ محاكي السيناريوهات التفاعلي (What-If Profit Simulator)
                    if st.session_state.get(f"show_profit_{i}"):
                        st.markdown("<div style='background:#0a0a0a; border:1px solid #333; padding:15px; border-radius:8px; margin-bottom:15px;'>", unsafe_allow_html=True)
                        st.markdown("<div style='color:#d4af37; font-family:\"Cinzel\", serif; margin-bottom:10px; font-size:0.9rem;'>🎛️ Interactive Margin Simulator</div>", unsafe_allow_html=True)
                        
                        try:
                            p = float(re.sub(r'[^\d.]', '', item.get('price', '0')))
                        except: p = 0.0
                        
                        cogs = p * 0.25
                        gateway = (p * 0.029) + 0.30
                        
                        col_s1, col_s2 = st.columns(2)
                        shipping = col_s1.slider("Shipping ($)", 0.0, float(p), float(p*0.15), key=f"ship_{i}")
                        cpa = col_s2.slider("Ad CPA ($)", 0.0, float(p), float(p*0.30), key=f"cpa_{i}")
                        
                        net = p - (cogs + shipping + gateway + cpa)
                        margin = (net / p) * 100 if p > 0 else 0
                        color = "#20c997" if net > 0 else "#dc3545"
                        
                        st.markdown(f"""
                        <div style='border-top:1px dashed #444; margin:10px 0; padding-top:10px; display:flex; justify-content:space-between; font-weight:600; font-size:1.1rem; font-family:"Montserrat", sans-serif;'>
                            <span style='color:#fff;'>NET PROFIT:</span> <span style='color:{color};'>${net:.2f} ({margin:.1f}%)</span>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<hr style='border-color:#222; margin:15px 0;'>", unsafe_allow_html=True)
                    
                    st.markdown("<div style='color:#888; font-size:0.7rem; margin-bottom:5px; letter-spacing:1px; text-transform:uppercase;'>THE CRAFT STUDIO</div>", unsafe_allow_html=True)
                    target_market = st.selectbox("", ["USA (English)", "Saudi Arabia (Arabic)", "UK (English)"], key=f"market_{i}", label_visibility="collapsed")
                    visual_style = st.selectbox("", ["Cinematic Luxury 🎬", "Authentic Lifestyle 📸"], key=f"style_{i}", label_visibility="collapsed")
                    
                    st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
                    if st.button("✦ Render Campaign Assets", key=f"btn_render_{i}", use_container_width=True):
                        with st.spinner("Crafting Localized Brand..."):
                            prompt = f"Act as a luxury brand strategist. Product: '{item.get('name')}'. Target Market: '{target_market}'. Visual Style: '{visual_style}'. Provide: 1. Brand Name 2. Tagline 3. Ad Copy in the NATIVE language/slang of '{target_market}'."
                            st.session_state[f"render_txt_{i}"] = call_gemini_direct(prompt)
                            
                            img_prompt = f"high end commercial photography of {specs}, cinematic studio lighting, dark luxury marble background, 8k resolution" if "Cinematic" in visual_style else f"authentic lifestyle photography of {specs}, user generated content style, realistic, held by a person in a cozy modern home environment, natural sunlight"
                            safe_hero_prompt = urllib.parse.quote_plus(img_prompt)
                            st.session_state[f"render_img_{i}"] = f"https://image.pollinations.ai/prompt/{safe_hero_prompt}?width=800&height=400&nologo=true&seed={i+500}"
                            st.balloons()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    if f"render_txt_{i}" in st.session_state:
                        st.markdown(f"""
                        <div style='background:#0d0d0d; padding:20px; border-radius:12px; border:1px solid #d4af37; margin-top:10px;'>
                            <div style='color:#d4af37; font-family:"Cinzel", serif; font-size:1rem; letter-spacing:2px; margin-bottom:15px; text-align:center;'>Campaign Assets</div>
                            <img src="{st.session_state[f'render_img_{i}']}" style="width:100%; border-radius:8px; margin-bottom:20px; border:1px solid #333;">
                            <div style='color:#ddd; font-size:0.9rem; line-height:1.6;'>{st.session_state[f'render_txt_{i}'].replace(chr(10), '<br>')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 🎬 زر توليد محاكي الفيديو (Video Ad Render)
                        if st.button("🎬 Render 15s TikTok Video", key=f"btn_vid_{i}"):
                            with st.spinner("Rendering Frames & Syncing Audio..."):
                                st.session_state[f"video_rendered_{i}"] = True
                                
                        if st.session_state.get(f"video_rendered_{i}"):
                            st.markdown(f"""
                            <div class="video-player">
                                <img src="{st.session_state[f'render_img_{i}']}">
                                <div class="video-play-btn">▶</div>
                                <div class="video-time">00:15</div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.success("✅ Video successfully rendered and synced with Voiceover!")
                        
                        campaign_data = json.dumps({
                            "WAFEEQ_AI_Export": True,
                            "Product_Name": item.get('name'),
                            "Target_Market": target_market,
                            "Visual_Style": visual_style,
                            "Hero_Image_URL": st.session_state[f"render_img_{i}"],
                            "Generated_Content": st.session_state[f"render_txt_{i}"]
                        }, indent=4, ensure_ascii=False)
                        
                        st.download_button(
                            label="⬇ Download Campaign (JSON) to Shopify",
                            data=campaign_data,
                            file_name=f"WAFEEQ_Campaign_{item.get('name').replace(' ', '_')}.json",
                            mime="application/json",
                            key=f"dl_{i}"
                        )

elif st.session_state.current_tab == 'shield':
    st.markdown('<div class="page-title">Trust Shield & Defender</div><div class="page-sub">AI-Powered Fraud Prevention & Legal Dispute Management</div>', unsafe_allow_html=True)
    st.markdown("<div class='panel-box'><div class='panel-header'>🚨 Active Dispute (Action Required)</div>", unsafe_allow_html=True)
    st.write("**Dispute #CB-9112** (Stripe Chargeback) - Reason: 'Product Not Received'")
    st.write("Customer: John Doe | Amount: $249.99 | Tracking: Delivered (DHL)")
    st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
    if st.button("✦ Generate Legal Response for Stripe"):
        with st.spinner("AI Lawyer drafting response..."):
            st.session_state.shield_response = call_gemini_direct("Act as an expert e-commerce legal responder. Write a strong, professional response to a Stripe chargeback for 'Product Not Received'. State that tracking shows it was delivered via DHL. Keep it concise, authoritative, and structured.")
    st.markdown("</div>", unsafe_allow_html=True)
    if "shield_response" in st.session_state:
        st.success("Draft Generated Successfully. Ready to submit to Stripe.")
        st.markdown(f"<div style='background:#111; padding:20px; border-left:4px solid #20c997; border-radius:8px; margin-top:10px; font-size:0.9rem;'>{st.session_state.shield_response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_tab == 'concierge':
    st.markdown('<div class="page-title">Omni-Channel Concierge</div><div class="page-sub">Empathetic AI Customer Support & Cart Rescue</div>', unsafe_allow_html=True)
    st.markdown("<div class='panel-box'><div class='panel-header'>🛒 Abandoned Cart Rescue (Live)</div>", unsafe_allow_html=True)
    st.write("**Customer:** Sarah M. (VIP Tier)")
    st.info("💬 **Customer Message:** 'I left the Elite Watch in my cart because I'm not sure if the ceramic scratches easily. Can you help?'")
    st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
    if st.button("✦ Generate Brand-Voice Response"):
        with st.spinner("Concierge is crafting a luxury reply..."):
            st.session_state.concierge_response = call_gemini_direct("Act as an elite luxury brand concierge. Respond to this customer: 'I left a watch in my cart, does the ceramic scratch easily?'. Use a highly sophisticated, empathetic, and reassuring tone to close the sale. Keep it short and elegant.")
    st.markdown("</div>", unsafe_allow_html=True)
    if "concierge_response" in st.session_state:
        st.markdown(f"<div style='background:#111; padding:20px; border-left:4px solid #d4af37; border-radius:8px; margin-top:10px; font-size:0.9rem;'>{st.session_state.concierge_response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_tab == 'growth':
    st.markdown('<div class="page-title">Multi-Dimensional Growth Engine</div><div class="page-sub">AI CMO: Automated Budget Scaling & Upsells</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: st.markdown("<div class='panel-box' style='text-align:center;'><div class='panel-header'>TikTok Ad Performance</div><h2 style='color:#20c997; font-family:Montserrat;'>320% ROI</h2><span style='color:#888;'>High Conversion Rate</span></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='panel-box' style='text-align:center;'><div class='panel-header'>Facebook Ad Performance</div><h2 style='color:#dc3545; font-family:Montserrat;'>110% ROI</h2><span style='color:#888;'>Declining Efficiency</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='panel-box'><div class='panel-header'>📈 AI CMO Recommendation</div>", unsafe_allow_html=True)
    st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
    if st.button("✦ Generate Growth & Upsell Strategy"):
        with st.spinner("AI CMO is calculating best moves..."):
            st.session_state.growth_response = call_gemini_direct("Act as an elite Chief Marketing Officer. The user's e-commerce store shows 320% ROI on TikTok and 110% on Facebook. Give a 1-sentence actionable advice on shifting the ad budget. Then, recommend ONE highly profitable UPSELL product they should add to the checkout page for a luxury watch brand.")
    st.markdown("</div>", unsafe_allow_html=True)
    if "growth_response" in st.session_state:
        st.success("Strategy Ready for Execution.")
        st.markdown(f"<div style='background:#111; padding:20px; border-left:4px solid #0dcaf0; border-radius:8px; margin-top:10px; font-size:0.9rem;'>{st.session_state.growth_response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)