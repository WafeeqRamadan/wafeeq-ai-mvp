import streamlit as st
import requests

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="WAFEEQ AI | Luxury Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إعداد مفتاح API (الاتصال المباشر)
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري في الخزنة.")
    st.stop()

# ==========================================
# 3. دالة الاتصال المباشر (تجاوزنا مكتبة جوجل تماماً)
# ==========================================
def generate_brand_content(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts":[{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        # إذا نجح الاتصال
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        # إذا كان المفتاح به مشكلة حقيقية
        else:
            return f"API Error ({response.status_code}): يرجى التأكد من أن المفتاح السري مفعل وليس منتهي الصلاحية."
    except Exception as e:
        return f"Network Error: {str(e)}"

# ==========================================
# 4. التصميم الفخم (Luxury UI)
# ==========================================
luxury_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #050505; 
    color: #e0e0e0;
    font-family: 'Lato', sans-serif;
}

#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] { display: none !important; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3.5rem; text-align: center; color: #ffffff; margin-top: 1rem; }
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card { background-color: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 12px; padding: 20px; transition: 0.3s; height: 220px; text-align: center; }
.platform-card:hover { border-color: #d4af37; background-color: #121212; transform: translateY(-5px); }
.platform-icon { font-size: 2.5rem; color: #d4af37; margin-bottom: 10px; }
.platform-name { font-size: 1.5rem; font-weight: 700; color: #fff; }

div.stButton > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border: none; border-radius: 4px; width: 100%; padding: 10px; transition: 0.3s; }
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px; }
.logo-text span { color: #d4af37; }
</style>
"""
st.markdown(luxury_style, unsafe_allow_html=True)

# ==========================================
# 5. محرك التطبيق
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

db = {
    "Amazon": [
        {"id": "a1", "name": "Minimalist Ceramic Watch", "price": "$120", "score": "97", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"id": "a2", "name": "Handcrafted Leather Bag", "price": "$250", "score": "94", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"}
    ]
}

if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    st.write("---")
    cols = st.columns(3)
    platforms = [("fa-brands fa-amazon", "Amazon"), ("fa-brands fa-tiktok", "TikTok Shop"), ("fa-solid fa-cart-shopping", "AliExpress")]
    
    for i, (icon, name) in enumerate(platforms):
        with cols[i]:
            st.markdown(f'<div class="platform-card"><div class="platform-icon"><i class="{icon}"></i></div><div class="platform-name">{name}</div></div>', unsafe_allow_html=True)
            if st.button(f"Explore {name}", key=f"p_{i}"):
                st.session_state.platform = name
                st.session_state.page = 'details'
                st.rerun()

elif st.session_state.page == 'details':
    if st.button("← Back to Platforms"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2>{st.session_state.platform} <span style='color:#d4af37;'>Trending Radar</span></h2>", unsafe_allow_html=True)
    
    items = db.get(st.session_state.platform, db["Amazon"])
    cols = st.columns(2)
    
    for i, item in enumerate(items):
        with cols[i]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"### {item['name']}")
            st.markdown(f"<span style='color:#d4af37; font-weight:bold;'>{item['price']}</span> | Trend: {item['score']}", unsafe_allow_html=True)
            
            if st.button(f"✨ Build {item['name']} Brand", key=f"btn_{i}"):
                with st.spinner("AI is crafting your luxury strategy..."):
                    # استخدام الاتصال المباشر الخارق
                    prompt = f"Act as a luxury brand strategist. Suggest an elegant brand name and a short premium tagline for: {item['name']}."
                    result = generate_brand_content(prompt)
                    
                    if "Error" in result:
                        st.error(result)
                    else:
                        st.session_state[f"res_{i}"] = result
                        st.balloons()
            
            if f"res_{i}" in st.session_state:
                st.markdown("---")
                st.info(st.session_state[f"res_{i}"])