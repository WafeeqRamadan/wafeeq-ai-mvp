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
# 2. فحص والاتصال بالذكاء الاصطناعي
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    try:
        genai.configure(api_key=api_key)
        # استخدام موديل Flash لأنه الأسرع والأكثر استقراراً للنسخ الأولية
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"❌ فشل في تهيئة النظام: {e}")
else:
    st.error("⚠️ لم يتم العثور على المفتاح في الخزنة! تأكد من إضافته في Secrets باسم GOOGLE_API_KEY")
    st.stop()

# ==========================================
# 3. CSS الفخامة والذهبي (Luxury UI)
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
    font-size: 4rem;
    text-align: center;
    color: #ffffff;
    margin-top: 1rem;
}
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card {
    background-color: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-radius: 15px;
    padding: 25px;
    transition: 0.4s;
    height: 280px;
    margin-bottom: 20px;
}
.platform-card:hover { border-color: #d4af37; background-color: #121212; transform: translateY(-5px); }
.platform-icon { font-size: 2.2rem; color: #d4af37; margin-bottom: 15px; }
.platform-name { font-size: 1.5rem; font-weight: 700; color: #fff; }
.platform-stats { color: #d4af37; font-weight: 700; font-size: 0.8rem; margin-top: 10px; }

div.stButton > button {
    background-color: #d4af37;
    color: #000 !important;
    font-weight: 700;
    border: none;
    border-radius: 4px;
    width: 100%;
    transition: 0.3s;
}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px; }
.logo-text span { color: #d4af37; }
</style>
"""
st.markdown(luxury_style, unsafe_allow_html=True)

# ==========================================
# 4. التنقل وقاعدة البيانات
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

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    
    platforms = [
        {"icon": "fa-brands fa-amazon", "name": "Amazon", "stats": "2.4M+ Items"},
        {"icon": "fa-brands fa-tiktok", "name": "TikTok Shop", "stats": "980K+ Items"},
        {"icon": "fa-solid fa-cart-shopping", "name": "AliExpress", "stats": "1.8M+ Items"}
    ]
    
    cols = st.columns(3)
    for i, p in enumerate(platforms):
        with cols[i]:
            st.markdown(f"""
            <div class="platform-card">
                <div class="platform-icon"><i class="{p['icon']}"></i></div>
                <div class="platform-name">{p['name']}</div>
                <div class="platform-stats"><i class="fa-solid fa-bolt"></i> {p['stats']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore {p['name']}", key=f"p_{i}"):
                st.session_state.platform = p['name']
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة الرادار ---
elif st.session_state.page == 'details':
    if st.button("← Back to Platforms"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2>{st.session_state.platform} <span style='color:#d4af37;'>Trending Radar</span></h2>", unsafe_allow_html=True)
    
    items = db.get(st.session_state.platform, db["Amazon"])
    cols = st.columns(3)
    
    for i, item in enumerate(items):
        with cols[i % 3]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"### {item['name']}")
            st.markdown(f"<span style='color:#d4af37; font-weight:bold;'>{item['price']}</span> | Trend: {item['score']}", unsafe_allow_html=True)
            
            # محرك توليد البراند
            if st.button(f"✨ Build {item['name']} Brand", key=f"btn_{i}"):
                with st.spinner("Creating your luxury strategy..."):
                    try:
                        # طلب بسيط من الذكاء الاصطناعي
                        prompt = f"Act as a luxury brand expert. For the product '{item['name']}', suggest a premium brand name and a short tagline. Be brief."
                        response = model.generate_content(prompt)
                        st.session_state[f"res_{i}"] = response.text
                        st.toast("Success! Brand strategy generated.", icon="✅")
                    except Exception as e:
                        st.error(f"❌ خطأ من Google: {str(e)}")
                        st.info("نصيحة: تأكد أن مفتاح API الذي نسخته هو مفتاح 'Gemini' وليس خدمة أخرى.")
            
            if f"res_{i}" in st.session_state:
                st.markdown("---")
                st.info(st.session_state[f"res_{i}"])