
import streamlit as st
import requests
import json
import urllib.parse
import re

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | Live Market Radar", page_icon="👑", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري في إعدادات الخزنة.")
    st.stop()

# ==========================================
# 2. محرك الذكاء الاصطناعي (الاتصال المباشر الصارم)
# ==========================================
@st.cache_data(ttl=3600)
def get_best_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models = res.json().get('models', [])
            valid_models = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', []) and 'vision' not in m['name'] and 'aqa' not in m['name'] and 'embedding' not in m['name'] and 'audio' not in m['name']]
            # إعطاء الأولوية القصوى للموديلات السريعة الحديثة
            valid_models.sort(key=lambda x: (
                0 if '2.5-flash' in x else
                1 if '2.0-flash' in x else 
                2 if '1.5-flash' in x else 
                3 if 'flash' in x else 4, x))
            return valid_models
        return []
    except:
        return []

def call_gemini_direct(prompt):
    models = get_best_models()
    if not models: return "Error: No valid models found. Check API key or Region."
    
    last_err = ""
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        try:
            res = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                last_err = f"{res.status_code} - {res.text}"
        except Exception as e:
            last_err = str(e)
            continue
    return f"Error: {last_err}"

# ==========================================
# 3. محرك الرادار (مع معالجة أخطاء JSON)
# ==========================================
def fetch_live_trends(niche, platform):
    prompt = f"""
    Act as an expert e-commerce product researcher. Find 2 currently highly trending and profitable products in the '{niche}' niche on {platform}.
    Return ONLY a valid JSON array. Do not include markdown formatting or backticks.
    Format exactly like this:
    [
      {{"name": "Product 1 Name", "price": "$XX.XX", "score": "98", "keyword": "Dress"}},
      {{"name": "Product 2 Name", "price": "$YY.YY", "score": "95", "keyword": "Watch"}}
    ]
    IMPORTANT: "keyword" MUST be exactly ONE simple English word describing the item (e.g. Mug, Shirt, Lamp).
    """
    response = call_gemini_direct(prompt)
    
    if "Error:" in response:
        st.error(f"⚠️ فشل الاتصال بخوادم جوجل: {response}")
        return None
        
    try:
        clean_json = response.replace('```json', '').replace('```', '').strip()
        match = re.search(r'\[.*\]', clean_json, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(clean_json)
    except Exception as e:
        st.error(f"⚠️ فشل في قراءة الرد. الرد الأصلي كان:\n{response}")
        return None

# ==========================================
# 4. التصميم الفاخر (CSS)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Lato', sans-serif; }
#MainMenu, footer, header { visibility: hidden !important; display: none !important; }
[data-testid="stDecoration"], [class*="viewerBadge"], a[href^="https://streamlit.io/cloud"] { display: none !important; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3.5rem; text-align: center; color: #ffffff; margin-top: 2rem; margin-bottom: 3rem;}
.hero-title span { color: #d4af37; font-style: italic; }

div.stButton > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border: none; border-radius: 6px; padding: 15px; transition: 0.3s; font-size: 1.1rem;}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); transform: translateY(-2px);}

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 15px 0; border-bottom: 1px solid #222; margin-bottom: 2rem;}
.logo-text span { color: #d4af37; }

.stTextInput input, .stSelectbox div[data-baseweb="select"] > div { background-color: #111 !important; color: #fff !important; border: 1px solid #333 !important; border-radius: 6px !important; padding: 10px !important;}
.stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus { border-color: #d4af37 !important; box-shadow: 0 0 5px rgba(212, 175, 55, 0.5) !important; }

img { border-radius: 8px; border: 1px solid #333; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. الواجهة والتفاعل
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Live Trend Radar<br>Across <span>Any Niche</span></div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #ccc; font-weight: 300; margin-bottom: 30px;'>🔍 What market are we analyzing today?</h4>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            niche_input = st.text_input("Niche", placeholder="e.g., Fashion, Tech Gadgets, Beauty...", label_visibility="collapsed")
        with col2:
            platform_input = st.selectbox("Platform", ["Amazon", "TikTok Shop", "AliExpress"], label_visibility="collapsed")
        
        st.write("")
        if st.button("🚀 Scan Live Market", use_container_width=True):
            if niche_input:
                st.session_state.niche = niche_input
                st.session_state.platform = platform_input
                st.session_state.page = 'results'
                st.rerun()
            else:
                st.warning("⚠️ Please enter a niche to scan.")

elif st.session_state.page == 'results':
    if st.button("← Back to Radar", use_container_width=False):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2 style='margin-top:20px;'>Live Radar: <span style='color:#d4af37;'>'{st.session_state.niche}'</span> on {st.session_state.platform}</h2>", unsafe_allow_html=True)
    st.write("---")
    
    with st.spinner("📡 AI is intercepting live market data..."):
        if 'live_data' not in st.session_state or st.session_state.get('last_niche') != st.session_state.niche:
            data = fetch_live_trends(st.session_state.niche, st.session_state.platform)
            st.session_state.live_data = data
            st.session_state.last_niche = st.session_state.niche

    if not st.session_state.live_data:
        st.info("لم يتم جلب المنتجات. يرجى التحقق من رسالة الخطأ أعلاه وإعادة المحاولة.")
    else:
        cols = st.columns(2)
        for i, item in enumerate(st.session_state.live_data):
            with cols[i % 2]:
                
                # 🛡️ توليد صورة فخمة 100% موثوقة (خلفية سوداء + نص ذهبي)
                raw_keyword = item.get('keyword', 'Product')
                clean_keyword = re.sub(r'[^a-zA-Z0-9]', '', raw_keyword).capitalize()
                if not clean_keyword: clean_keyword = 'Trend'
                
                img_url = f"https://placehold.co/600x400/111111/d4af37?text={clean_keyword}"
                st.image(img_url, use_container_width=True)
                
                st.markdown(f"<h3 style='margin-top:15px;'>{item['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#d4af37; font-weight:bold; font-size:1.2rem;'>{item['price']}</span> | Trend Score: {item['score']} ↗", unsafe_allow_html=True)
                
                if st.button(f"✨ Build Brand Strategy", key=f"btn_{i}", use_container_width=True):
                    with st.spinner("Crafting your luxury brand..."):
                        prompt = f"""Act as a high-end luxury brand strategist. For the product '{item['name']}', provide:
                        1. A premium Brand Name.
                        2. A short, elegant Tagline.
                        3. A brief luxury description targeting high-end clientele."""
                        
                        result = call_gemini_direct(prompt)
                        
                        if "Error" in result:
                            st.error(result)
                        else:
                            st.session_state[f"res_{i}"] = result
                            st.balloons()
                
                if f"res_{i}" in st.session_state:
                    st.markdown(f"<div style='background-color:#111; padding:20px; border-radius:8px; border-left:4px solid #d4af37; margin-top:15px; color:#ddd; line-height:1.6;'>{st.session_state[f'res_{i}']}</div>", unsafe_allow_html=True)