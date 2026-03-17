import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# 1. إعدادات الصفحة الأساسية
# ==========================================
st.set_page_config(
    page_title="WAFEEQ AI | E-Commerce Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. التحقق من مفتاح الـ API (الخزنة)
# ==========================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ لم يتم العثور على مفتاح API! يرجى إضافته في إعدادات Streamlit Cloud (Secrets).")
    st.stop()
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-pro')

# ==========================================
# 3. CSS المتقدم وجلب الأيقونات (Luxury UI)
# ==========================================
luxury_css = """
<style>
/* جلب خطوط جوجل ومكتبة FontAwesome للأيقونات */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080808; 
    color: #e0e0e0;
    font-family: 'Lato', sans-serif;
}

/* إخفاء زوائد ستريمليت */
#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] {
    display: none !important;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    text-align: center;
    color: #ffffff;
    margin-top: 2rem;
}

.hero-title span { color: #d4af37; font-style: italic; }

/* تنسيق بطاقات المنصات */
.platform-card {
    background-color: #121212;
    border: 1px solid #222222;
    border-radius: 12px;
    padding: 25px;
    text-align: left;
    transition: all 0.3s ease;
    height: 320px;
    margin-bottom: 20px;
}

.platform-card:hover {
    border-color: #d4af37;
    background-color: #161616;
    transform: translateY(-5px);
}

.platform-icon {
    font-size: 2rem;
    color: #d4af37;
    margin-bottom: 20px;
}

.platform-name { font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 10px; }
.platform-desc { color: #777; font-size: 0.9rem; margin-bottom: 15px; }
.platform-stats { color: #d4af37; font-weight: 700; font-size: 0.8rem; }

/* أزرار الإطلاق الذهبية */
div.stButton > button {
    background-color: #d4af37;
    color: #000 !important;
    font-weight: 700;
    border: none;
    border-radius: 5px;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #fff;
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
}

/* شعار الموقع */
.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; }
.logo-text span { color: #d4af37; }
</style>
"""
st.markdown(luxury_css, unsafe_allow_html=True)

# ==========================================
# 4. إدارة الصفحات والبيانات
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

# بيانات المنتجات (روابط صور أكثر استقراراً)
db_products = {
    "Amazon": [
        {"id": "a1", "name": "Modern Minimalist Watch", "category": "ACCESSORIES", "score": "97", "price": "$120", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
        {"id": "a2", "name": "Premium Leather Bag", "category": "FASHION", "score": "94", "price": "$250", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500"},
        {"id": "a3", "name": "Noise Cancelling Buds", "category": "TECH", "score": "91", "price": "$199", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"}
    ],
    "TikTok Shop": [
        {"id": "t1", "name": "LED Sunset Lamp", "category": "DECOR", "score": "99", "price": "$25", "img": "https://images.unsplash.com/photo-1565814329452-e1efa11c5e8d?w=500"},
        {"id": "t2", "name": "Cloud Slippers", "category": "LIFESTYLE", "score": "98", "price": "$19", "img": "https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=500"}
    ]
}

# ==========================================
# الصفحة الرئيسية (Landing)
# ==========================================
if st.session_state.current_page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Select a marketplace to explore live data and generate luxury brands.</p>", unsafe_allow_html=True)
    
    platforms = [
        {"icon": "fa-brands fa-amazon", "name": "Amazon", "desc": "Global marketplace leader.", "stats": "2.4M+ Items"},
        {"icon": "fa-solid fa-cart-shopping", "name": "AliExpress", "desc": "Direct supplier source.", "stats": "1.8M+ Items"},
        {"icon": "fa-brands fa-tiktok", "name": "TikTok Shop", "desc": "Viral social commerce.", "stats": "980K+ Items"},
        {"icon": "fa-solid fa-store", "name": "Walmart", "desc": "Top US retail trends.", "stats": "1.2M+ Items"},
        {"icon": "fa-brands fa-etsy", "name": "Etsy", "desc": "Unique handmade goods.", "stats": "650K+ Items"},
        {"icon": "fa-brands fa-ebay", "name": "eBay", "desc": "Direct and auction sales.", "stats": "1.5M+ Items"}
    ]
    
    col1, col2, col3 = st.columns(3)
    grid = [col1, col2, col3, col1, col2, col3]
    
    for i, p in enumerate(platforms):
        with grid[i]:
            card_html = f"""
            <div class="platform-card">
                <div class="platform-icon"><i class="{p['icon']}"></i></div>
                <div class="platform-name">{p['name']}</div>
                <div class="platform-desc">{p['desc']}</div>
                <div class="platform-stats"><i class="fa-solid fa-bolt"></i> {p['stats']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"Explore {p['name']}", key=f"btn_{i}"):
                st.session_state.selected_p = p['name']
                st.session_state.current_page = 'details'
                st.rerun()

# ==========================================
# صفحة المنتجات (Details)
# ==========================================
elif st.session_state.current_page == 'details':
    if st.button("← Back"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown(f"<h2>{st.session_state.selected_p} <span style='color:#d4af37;'>Trending Radar</span></h2>", unsafe_allow_html=True)
    
    items = db_products.get(st.session_state.selected_p, db_products["Amazon"])
    cols = st.columns(3)
    
    for i, item in enumerate(items):
        with cols[i % 3]:
            # عرض الصورة باستخدام أمر ستريمليت المباشر (أكثر استقراراً)
            st.image(item['img'], use_container_width=True)
            st.markdown(f"### {item['name']}")
            st.markdown(f"<span style='color:#d4af37; font-weight:bold;'>{item['price']}</span> | Score: {item['score']}", unsafe_allow_html=True)
            
            if st.button(f"✨ Build {item['name']} Brand", key=f"gen_{i}"):
                with st.spinner("AI Strategist is working..."):
                    prompt = f"Create a luxury brand name and slogan for this product: {item['name']}"
                    try:
                        res = model.generate_content(prompt)
                        st.session_state[f"res_{i}"] = res.text
                    except:
                        st.error("خطأ في المفتاح السري! تأكد من وضعه في إعدادات Streamlit.")
            
            if f"res_{i}" in st.session_state:
                st.info(st.session_state[f"res_{i}"])