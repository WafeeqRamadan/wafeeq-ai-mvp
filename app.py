import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="WAFEEQ AI | E-Commerce Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. الربط بالخزنة السرية (Secrets)
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("⚠️ لم يتم العثور على المفتاح في Secrets! يرجى إضافته في إعدادات Streamlit.")
    st.stop()

# ==========================================
# 3. CSS الفخامة والذهبي (Luxury UI)
# ==========================================
luxury_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080808; 
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
    background-color: #121212;
    border: 1px solid #222222;
    border-radius: 12px;
    padding: 25px;
    transition: 0.3s;
    height: 300px;
    margin-bottom: 20px;
}
.platform-card:hover { border-color: #d4af37; background-color: #161616; transform: translateY(-5px); }
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
st.markdown(luxury_css, unsafe_allow_html=True)

# ==========================================
# 4. التنقل بين الصفحات
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

# بيانات المنتجات
db = {
    "Amazon": [
        {"id": "a1", "name": "Modern Minimalist Watch", "price": "$120", "score": "97", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"id": "a2", "name": "Premium Leather Bag", "price": "$250", "score": "94", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"},
        {"id": "a3", "name": "ANC Wireless Buds", "price": "$199", "score": "91", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600"}
    ],
    "TikTok Shop": [
        {"id": "t1", "name": "Sunset Projection Lamp", "price": "$25", "score": "99", "img": "https://images.unsplash.com/photo-1565814329452-e1efa11c5e8d?w=600"},
        {"id": "t2", "name": "Cloud Comfort Slippers", "price": "$19", "score": "98", "img": "https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=600"}
    ]
}

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    
    platforms = [
        {"icon": "fa-brands fa-amazon", "name": "Amazon", "stats": "2.4M+ Items"},
        {"icon": "fa-solid fa-cart-shopping", "name": "AliExpress", "stats": "1.8M+ Items"},
        {"icon": "fa-brands fa-tiktok", "name": "TikTok Shop", "stats": "980K+ Items"},
        {"icon": "fa-solid fa-store", "name": "Walmart", "stats": "1.2M+ Items"},
        {"icon": "fa-brands fa-etsy", "name": "Etsy", "stats": "650K+ Items"},
        {"icon": "fa-brands fa-ebay", "name": "eBay", "stats": "1.5M+ Items"}
    ]
    
    cols = st.columns(3)
    for i, p in enumerate(platforms):
        with cols[i % 3]:
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

# --- صفحة التفاصيل ---
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
            
            if st.button(f"✨ Build {item['name']} Brand", key=f"btn_{i}"):
                with st.spinner("Crafting your luxury brand strategy..."):
                    try:
                        prompt = f"Create a luxury brand name, tagline, and 2-sentence sales pitch for: {item['name']}. Focus on premium positioning."
                        response = model.generate_content(prompt)
                        st.session_state[f"res_{i}"] = response.text
                    except Exception as e:
                        st.error("خطأ! تأكد من صحة مفتاح API في الإعدادات.")
            
            if f"res_{i}" in st.session_state:
                st.markdown("---")
                st.info(st.session_state[f"res_{i}"])