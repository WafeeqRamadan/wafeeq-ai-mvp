import streamlit as st
import requests
import json
import urllib.parse
import re

# ==========================================
# 1. الإعدادات الأساسية
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | Luxury Intelligence", page_icon="✦", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري في الخزنة.")
    st.stop()

# ==========================================
# 2. محرك الذكاء الاصطناعي (API)
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
    Find 3 highly trending and profitable products in the '{niche}' niche on {platform}.
    Return ONLY a valid JSON array.
    [
      {{"name": "Chronograph Elite Watch", "price": "$249.99", "score": "97", "category": "ACCESSORIES", "keyword": "Watch"}},
      {{"name": "Minimalist Leather Tote", "price": "$189.00", "score": "94", "category": "FASHION", "keyword": "LeatherTote"}},
      {{"name": "Wireless ANC Earbuds Pro", "price": "$159.99", "score": "91", "category": "ELECTRONICS", "keyword": "Earbuds"}}
    ]
    IMPORTANT: "keyword" MUST be exactly ONE simple English word describing the item for image generation.
    """
    response = call_gemini_direct(prompt)
    if "Error:" in response: return None
    try:
        clean_json = response.replace('```json', '').replace('```', '').strip()
        match = re.search(r'\[.*\]', clean_json, re.DOTALL)
        return json.loads(match.group(0)) if match else json.loads(clean_json)
    except: return None

# ==========================================
# 3. التصميم الفاخر (CSS المطابق للصور)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #0a0a0a; color: #e0e0e0; font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* Navbar Styling */
.custom-navbar { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 40px; }
.nav-logo { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; line-height: 1; letter-spacing: 2px;}
.nav-logo span { color: #d4af37; }
.nav-sub { font-family: 'Inter', sans-serif; font-size: 0.6rem; color: #666; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px;}
.nav-buttons { display: flex; gap: 15px; }
.btn-login { background: transparent; border: 1px solid #333; color: #fff; padding: 8px 20px; border-radius: 6px; font-size: 0.9rem; cursor: pointer;}
.btn-started { background: #d4af37; border: none; color: #000; padding: 8px 20px; border-radius: 6px; font-weight: 600; font-size: 0.9rem; cursor: pointer;}

/* Hero Section */
.hero-pill { background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.3); color: #d4af37; padding: 6px 15px; border-radius: 20px; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; display: inline-block; margin-bottom: 20px;}
.hero-title { font-family: 'Playfair Display', serif; font-size: 4.5rem; text-align: center; color: #ffffff; line-height: 1.1; margin-bottom: 20px;}
.hero-title span { color: #d4af37; font-style: italic; font-weight: 400;}
.hero-subtitle { text-align: center; color: #888; font-size: 1.1rem; max-width: 600px; margin: 0 auto 40px auto; line-height: 1.6;}

/* Platform Cards */
.platform-grid-card { background-color: #111; border: 1px solid #222; border-radius: 12px; padding: 25px; transition: 0.3s; height: 100%; position: relative;}
.platform-grid-card:hover { border-color: #d4af37; background-color: #151515; }
.p-icon { width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem; margin-bottom: 20px;}
.p-icon.amazon { background: rgba(212, 175, 55, 0.1); color: #d4af37; }
.p-icon.ali { background: rgba(220, 53, 69, 0.1); color: #dc3545; }
.p-icon.tiktok { background: rgba(32, 201, 151, 0.1); color: #20c997; }
.live-data { position: absolute; top: 25px; right: 25px; font-size: 0.7rem; color: #d4af37; letter-spacing: 1px; display: flex; align-items: center; gap: 5px;}
.live-data::before { content: ''; width: 6px; height: 6px; background-color: #d4af37; border-radius: 50%; display: inline-block;}
.p-title { font-size: 1.5rem; color: #fff; font-weight: 600; margin-bottom: 8px;}
.p-desc { color: #666; font-size: 0.9rem; margin-bottom: 25px;}
.p-stats { color: #d4af37; font-size: 0.85rem; font-weight: 600; display: flex; justify-content: space-between; align-items: center;}

/* Product Cards */
.radar-header { display: flex; align-items: center; gap: 15px; margin-bottom: 5px;}
.radar-sub { color: #666; font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px;}
.product-card { background: #111; border: 1px solid #222; border-radius: 16px; padding: 15px; margin-bottom: 15px;}
.product-img { width: 100%; height: 220px; object-fit: cover; border-radius: 10px; margin-bottom: 15px;}
.product-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;}
.p-category { color: #666; font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase;}
.p-score { border: 1px solid #333; color: #d4af37; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem;}
.p-name { color: #fff; font-size: 1.2rem; font-weight: 600; margin-bottom: 10px; line-height: 1.3;}
.p-price { color: #d4af37; font-size: 1.3rem; font-family: 'Playfair Display', serif;}

/* Buttons */
div.stButton > button { background-color: #c5a059; color: #000 !important; font-weight: 600; border: none; border-radius: 8px; padding: 12px; transition: 0.3s; width: 100%;}
div.stButton > button:hover { background-color: #e8c37b; transform: translateY(-2px);}
.search-input-container { max-width: 500px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. واجهة المستخدم والتنقل
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'landing'

# شريط التنقل العلوي (Navbar)
st.markdown("""
<div class="custom-navbar">
    <div class="logo-box">
        <div class="nav-logo">WAFEEQ <span>AI</span></div>
        <div class="nav-sub">FROM TREND TO BRAND IN ONE CLICK</div>
    </div>
    <div class="nav-buttons">
        <button class="btn-login">Login</button>
        <button class="btn-started">Get Started — Free</button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- الصفحة الافتتاحية (Landing Page) ---
if st.session_state.page == 'landing':
    st.markdown("""
    <div style="text-align: center;">
        <div class="hero-pill">● AI-POWERED E-COMMERCE INTELLIGENCE</div>
        <div class="hero-title">Discover Trending Products<br>Across <span>Every Platform</span></div>
        <div class="hero-subtitle">Real-time trend analysis and luxury brand content generation for the world's top e-commerce marketplaces. From product discovery to branded launch — in one click.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("✦ Start Finding Products — Free", use_container_width=True):
            st.session_state.page = 'platforms'
            st.rerun()

# --- صفحة اختيار المنصة (Platforms Page) ---
elif st.session_state.page == 'platforms':
    st.markdown('<div class="hero-title" style="font-size: 3rem; margin-top:0;">Choose Your <span>Platform</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Select a marketplace to explore trending products</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="search-input-container">', unsafe_allow_html=True)
    niche = st.text_input("", placeholder="Enter a niche (e.g. Fashion, Tech, Home)...", label_visibility="collapsed")
    st.markdown('</div><br>', unsafe_allow_html=True)
    
    platforms = [
        {"id": "A", "name": "Amazon", "desc": "World's largest e-commerce marketplace", "stats": "2.4M+ products", "class": "amazon"},
        {"id": "AE", "name": "AliExpress", "desc": "Direct suppliers from global manufacturers", "stats": "1.8M+ products", "class": "ali"},
        {"id": "TT", "name": "TikTok Shop", "desc": "Viral product discovery for Gen Z & beyond", "stats": "980K+ products", "class": "tiktok"}
    ]
    
    cols = st.columns(3)
    for i, p in enumerate(platforms):
        with cols[i]:
            st.markdown(f"""
            <div class="platform-grid-card">
                <div class="live-data">LIVE DATA</div>
                <div class="p-icon {p['class']}">{p['id']}</div>
                <div class="p-title">{p['name']}</div>
                <div class="p-desc">{p['desc']}</div>
                <div class="p-stats"><span>{p['stats']}</span> <span>→</span></div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore {p['name']}", key=f"btn_p_{i}"):
                st.session_state.platform = p['name']
                st.session_state.niche = niche if niche else "Luxury Goods"
                st.session_state.page = 'radar'
                st.rerun()

# --- صفحة الرادار والمنتجات (Radar Page) ---
elif st.session_state.page == 'radar':
    if st.button("← Back to Platforms"):
        st.session_state.page = 'platforms'
        st.rerun()
    
    # Header Section matches the 3rd image
    st.markdown(f"""
    <div class="radar-header">
        <div class="p-icon amazon" style="margin-bottom:0; width:35px; height:35px; font-size:1rem;">{st.session_state.platform[0]}</div>
        <span style="font-family:'Playfair Display', serif; font-size:2rem; color:#fff;">{st.session_state.platform} — <span style="color:#d4af37; font-style:italic;">Trending Products</span></span>
    </div>
    <div class="radar-sub">TOP PRODUCTS · RANKED BY AI TREND ANALYSIS IN '{st.session_state.niche.upper()}'</div>
    """, unsafe_allow_html=True)
    
    with st.spinner("📡 Intercepting live market data..."):
        if 'live_data' not in st.session_state or st.session_state.get('last_niche') != f"{st.session_state.niche}_{st.session_state.platform}":
            st.session_state.live_data = fetch_live_trends(st.session_state.niche, st.session_state.platform)
            st.session_state.last_niche = f"{st.session_state.niche}_{st.session_state.platform}"

    if not st.session_state.live_data:
        st.error("⚠️ AI is busy. Please try another niche or refresh.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(st.session_state.live_data):
            with cols[i % 3]:
                # Image Generation
                clean_keyword = re.sub(r'[^a-zA-Z0-9]', '', item.get('keyword', 'luxury'))
                safe_prompt = urllib.parse.quote_plus(f"high end commercial photography of {clean_keyword}, cinematic lighting, dark background, 8k")
                img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=400&height=300&nologo=true&seed={i+10}"
                
                # Product Card HTML
                st.markdown(f"""
                <div class="product-card">
                    <img src="{img_url}" class="product-img" onerror="this.src='https://placehold.co/400x300/111/d4af37?text={clean_keyword}';">
                    <div class="product-meta">
                        <span class="p-category">{item.get('category', 'TRENDING')}</span>
                        <span class="p-score">↗ {item.get('score', '95')}</span>
                    </div>
                    <div class="p-name">{item.get('name', 'Luxury Product')}</div>
                    <div class="p-price">{item.get('price', '$99.00')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✦ Generate Luxury Brand", key=f"btn_b_{i}"):
                    with st.spinner("Crafting brand strategy..."):
                        prompt = f"Act as a luxury brand strategist. For '{item.get('name')}', provide: 1. Brand Name 2. Tagline 3. Short luxury description."
                        res = call_gemini_direct(prompt)
                        st.session_state[f"res_{i}"] = res
                        st.balloons()
                
                if f"res_{i}" in st.session_state:
                    st.markdown(f"<div style='background:#111; padding:20px; border-radius:12px; border:1px solid #d4af37; margin-top:10px; color:#ddd; font-size:0.9rem;'>{st.session_state[f'res_{i}']}</div>", unsafe_allow_html=True)