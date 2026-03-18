import streamlit as st
import requests

# ==========================================
# 1. الإعدادات الأساسية
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | Luxury Intelligence", page_icon="✨", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري (GOOGLE_API_KEY) في الخزنة.")
    st.stop()

# ==========================================
# 2. العقل المدبر (الاتصال المستقر والسريع)
# ==========================================
@st.cache_data(ttl=3600)
def get_free_tier_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models = res.json().get('models', [])
            valid_models = []
            for m in models:
                name = m.get('name', '')
                methods = m.get('supportedGenerationMethods', [])
                if 'generateContent' in methods and 'vision' not in name and 'aqa' not in name and 'embedding' not in name:
                    valid_models.append(name)
            # وضع الموديلات المجانية والسريعة (Flash) في المقدمة لتجنب رسوم أو توقف
            valid_models.sort(key=lambda x: (0 if 'flash' in x.lower() else 1, x))
            return valid_models
        return []
    except:
        return []

def generate_brand_smart(prompt):
    models = get_free_tier_models()
    if not models:
        return "❌ لم نعثر على أي موديل صالح للعمل."
        
    for model_name in models:
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        try:
            res = requests.post(gen_url, headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return "❌ نعتذر، هناك ضغط على خوادم الذكاء الاصطناعي حالياً."

# ==========================================
# 3. التصميم الفاخر (Luxury UI & CSS)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Lato', sans-serif; }
#MainMenu, footer, header { visibility: hidden !important; display: none !important; }
[data-testid="stDecoration"], [class*="viewerBadge"], a[href^="https://streamlit.io/cloud"] { display: none !important; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3.5rem; text-align: center; color: #ffffff; margin-top: 1rem; margin-bottom: 2rem;}
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card { background-color: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 12px; padding: 25px; transition: 0.3s; text-align: center; height: 100%; margin-bottom: 15px;}
.platform-card:hover { border-color: #d4af37; background-color: #121212; transform: translateY(-5px); }
.platform-icon { font-size: 2.5rem; color: #d4af37; margin-bottom: 15px; }
.platform-name { font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 10px;}

div.stButton > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border: none; border-radius: 4px; padding: 10px 20px; transition: 0.3s; width: 100%;}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px 0; border-bottom: 1px solid #222; margin-bottom: 2rem;}
.logo-text span { color: #d4af37; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. محرك التطبيق وقاعدة البيانات
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

db = {
    "Amazon": [
        {"name": "Minimalist Ceramic Watch", "price": "$120", "score": "97", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"name": "Handcrafted Leather Bag", "price": "$250", "score": "94", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"}
    ]
}

# --- صفحة الأسواق ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products<br>Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    platforms = [("fa-brands fa-amazon", "Amazon"), ("fa-brands fa-tiktok", "TikTok Shop"), ("fa-solid fa-cart-shopping", "AliExpress")]
    
    for i, (icon, name) in enumerate(platforms):
        with cols[i]:
            st.markdown(f'<div class="platform-card"><div class="platform-icon"><i class="{icon}"></i></div><div class="platform-name">{name}</div></div>', unsafe_allow_html=True)
            if st.button(f"Explore {name}", key=f"p_{i}"):
                st.session_state.platform = name
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة المنتجات والذكاء الاصطناعي ---
elif st.session_state.page == 'details':
    if st.button("← Back to Platforms"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2>{st.session_state.platform} <span style='color:#d4af37;'>Trending Radar</span></h2>", unsafe_allow_html=True)
    st.write("---")
    
    items = db.get(st.session_state.platform, db["Amazon"])
    cols = st.columns(2)
    
    for i, item in enumerate(items):
        with cols[i]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"<h3 style='margin-top:15px;'>{item['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#d4af37; font-weight:bold; font-size:1.2rem;'>{item['price']}</span> | Trend Score: {item['score']}", unsafe_allow_html=True)
            
            if st.button(f"✨ Build Brand Strategy", key=f"btn_{i}"):
                with st.spinner("AI is crafting your luxury strategy..."):
                    prompt = f"""Act as a luxury brand strategist. For the product '{item['name']}', provide:
                    1. A sophisticated, premium Brand Name.
                    2. A short, elegant Tagline.
                    3. A one-paragraph luxury description targeting high-end clientele.
                    Make it sound highly professional and exclusive."""
                    
                    result = generate_brand_smart(prompt)
                    
                    if "❌" in result:
                        st.error(result)
                    else:
                        st.session_state[f"res_{i}"] = result
                        st.balloons()
            
            # عرض النتيجة في المربع ذو الإطار الذهبي
            if f"res_{i}" in st.session_state:
                st.markdown(f"<div style='background-color:#111; padding:20px; border-radius:8px; border-left:4px solid #d4af37; margin-top:15px; color:#ddd; line-height:1.6;'>{st.session_state[f'res_{i}']}</div>", unsafe_allow_html=True)