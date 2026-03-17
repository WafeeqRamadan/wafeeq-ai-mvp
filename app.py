import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. إعدادات الصفحة الفخمة
# ==========================================
st.set_page_config(
    page_title="WAFEEQ AI | Luxury Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. الربط بالذكاء الاصطناعي (تم تصحيح اسم الموديل)
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام الاسم الأكثر استقراراً للموديل لضمان عدم حدوث خطأ 404
        model = genai.GenerativeModel('gemini-pro') 
    except Exception as e:
        st.error(f"❌ فشل في تهيئة النظام: {e}")
else:
    st.error("⚠️ يرجى إضافة GOOGLE_API_KEY في Secrets.")
    st.stop()

# ==========================================
# 3. CSS الفخامة (Luxury UI)
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

#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] {
    display: none !important;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    text-align: center;
    color: #ffffff;
    margin-top: 1rem;
}
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card {
    background-color: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 20px;
    transition: 0.3s;
    height: 250px;
}
.platform-card:hover { border-color: #d4af37; background-color: #121212; }
.platform-icon { font-size: 2rem; color: #d4af37; margin-bottom: 10px; }

div.stButton > button {
    background-color: #d4af37;
    color: #000 !important;
    font-weight: 700;
    border: none;
    border-radius: 4px;
    width: 100%;
}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px; }
.logo-text span { color: #d4af37; }
</style>
"""
st.markdown(luxury_style, unsafe_allow_html=True)

# ==========================================
# 4. التنقل والمحتوى
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

db = {
    "Amazon": [
        {"id": "a1", "name": "Minimalist Ceramic Watch", "price": "$120", "score": "97", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"id": "a2", "name": "Handcrafted Leather Bag", "price": "$250", "score": "94", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"},
        {"id": "a3", "name": "Smart Espresso Station", "price": "$450", "score": "89", "img": "https://images.unsplash.com/photo-1517246286411-8bb31bf4148b?w=600"}
    ]
}

if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    platforms = [("fa-brands fa-amazon", "Amazon"), ("fa-brands fa-tiktok", "TikTok Shop"), ("fa-solid fa-cart-shopping", "AliExpress")]
    for i, (icon, name) in enumerate(platforms):
        with cols[i]:
            st.markdown(f'<div class="platform-card"><div class="platform-icon"><i class="{icon}"></i></div><div style="font-size:1.5rem; font-weight:700;">{name}</div></div>', unsafe_allow_html=True)
            if st.button(f"Explore {name}", key=f"p_{i}"):
                st.session_state.platform = name
                st.session_state.page = 'details'
                st.rerun()

elif st.session_state.page == 'details':
    if st.button("← Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    items = db.get(st.session_state.platform, db["Amazon"])
    cols = st.columns(3)
    
    for i, item in enumerate(items):
        with cols[i]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"### {item['name']}")
            if st.button(f"✨ Build {item['name']} Brand", key=f"btn_{i}"):
                with st.spinner("Creating Brand..."):
                    try:
                        # طلب بسيط من الموديل المستقر
                        response = model.generate_content(f"Suggest a luxury brand name and a one-sentence tagline for: {item['name']}")
                        st.session_state[f"res_{i}"] = response.text
                    except Exception as e:
                        st.error(f"⚠️ تفاصيل الخطأ: {e}")
            
            if f"res_{i}" in st.session_state:
                st.markdown("---")
                st.info(st.session_state[f"res_{i}"])