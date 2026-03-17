import streamlit as st
import google.generativeai as genai
import time

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="WAFEEQ AI | E-Commerce Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS المتقدم: الفخامة والذهبي (Luxury UI) ---
luxury_css = """
<style>
/* استيراد الخطوط: Playfair للعناوين، و Lato للنصوص */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

/* الخلفية واللون الأساسي */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #080808; /* أسود عميق جداً */
    color: #e0e0e0;
    font-family: 'Lato', sans-serif;
}

/* إخفاء عناصر Streamlit المزعجة */
#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] {
    display: none !important;
}

/* --- تنسيقات العناوين (Playfair Display) --- */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4.5rem;
    font-weight: 400;
    text-align: center;
    color: #ffffff;
    line-height: 1.2;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.hero-title span {
    color: #d4af37; /* لون ذهبي فاخر */
    font-style: italic;
}

.hero-subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #888888;
    max-width: 600px;
    margin: 0 auto 3rem auto;
    line-height: 1.6;
    font-weight: 300;
}

/* --- تنسيقات الأزرار الذهبية --- */
div.stButton > button {
    background-color: #d4af37;
    color: #000000 !important;
    font-family: 'Lato', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 4px;
    padding: 12px 24px;
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #bfa136;
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    border: none;
}

/* الزر الثانوي (الأسود ذو الحواف الذهبية) */
div.stButton.secondary-btn > button {
    background-color: transparent;
    color: #d4af37 !important;
    border: 1px solid #d4af37;
}

div.stButton.secondary-btn > button:hover {
    background-color: rgba(212, 175, 55, 0.1);
}

/* --- بطاقات المنصات (Platforms Grid) --- */
.platform-card {
    background-color: #121212;
    border: 1px solid #222222;
    border-radius: 8px;
    padding: 30px 20px;
    text-align: left;
    transition: all 0.3s ease;
    cursor: pointer;
    height: 100%;
}

.platform-card:hover {
    border-color: #d4af37;
    background-color: #161616;
}

.platform-icon {
    width: 40px;
    height: 40px;
    background-color: #1a1a1a;
    color: #d4af37;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-bottom: 20px;
    font-size: 1.2rem;
}

.platform-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}

.platform-desc {
    font-size: 0.9rem;
    color: #777777;
    margin-bottom: 20px;
    min-height: 40px;
}

.platform-stats {
    font-size: 0.8rem;
    color: #d4af37;
    font-weight: 700;
}

/* --- شعار الموقع أعلى اليسار --- */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #222222;
    margin-bottom: 2rem;
}

.logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 2px;
}
.logo-text span {
    color: #d4af37;
}
</style>
"""
st.markdown(luxury_css, unsafe_allow_html=True)

# --- 3. إدارة حالة التطبيق (للتنقل بين الصفحات) ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# --- 4. الشريط العلوي (Navigation) ---
st.markdown("""
<div class="top-nav">
    <div class="logo-text">WAFEEQ <span>AI</span></div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# الصفحة الرئيسية (Landing Page & Platforms)
# ==========================================
if st.session_state.current_page == 'home':
    
    # قسم الـ Hero (العنوان الضخم)
    st.markdown("""
    <div class="hero-title">Discover Trending Products<br>Across <span>Every Platform</span></div>
    <div class="hero-subtitle">Real-time trend analysis and luxury brand content generation for the world's top e-commerce marketplaces. From product discovery to branded launch — in one click.</div>
    """, unsafe_allow_html=True)
    
    # مساحة فارغة للترتيب
    st.write("")
    st.write("")
    
    # عنوان قسم المنصات
    st.markdown("<h3 style='text-align: center; font-family: \"Playfair Display\", serif; font-weight: 400; color: #fff; margin-bottom: 2rem;'>Choose Your <span style='color:#d4af37; font-style:italic;'>Platform</span></h3>", unsafe_allow_html=True)
    
    # بيانات المنصات
    platforms = [
        {"icon": "A", "name": "Amazon", "desc": "World's largest e-commerce marketplace", "stats": "2.4M+ products"},
        {"icon": "AE", "name": "AliExpress", "desc": "Direct suppliers from global manufacturers", "stats": "1.8M+ products"},
        {"icon": "TT", "name": "TikTok Shop", "desc": "Viral product discovery for Gen Z & beyond", "stats": "980K+ products"},
        {"icon": "W", "name": "Walmart", "desc": "Dominant US retail marketplace", "stats": "1.2M+ products"},
        {"icon": "Et", "name": "Etsy", "desc": "Handmade, vintage & unique products", "stats": "650K+ products"},
        {"icon": "eB", "name": "eBay", "desc": "Auctions, collectibles & direct sales", "stats": "1.5M+ products"}
    ]
    
    # بناء شبكة المنصات (3 أعمدة × صفين)
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3]
    
    for i, p in enumerate(platforms):
        with cols[i]:
            # نرسم البطاقة كـ HTML
            card_html = f"""
            <div class="platform-card">
                <div style="text-align: right; font-size: 0.7rem; color: #d4af37; margin-bottom: 10px;">● LIVE DATA</div>
                <div class="platform-icon">{p['icon']}</div>
                <div class="platform-name">{p['name']}</div>
                <div class="platform-desc">{p['desc']}</div>
                <div class="platform-stats">{p['stats']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            # زر غير مرئي تقريباً فوق البطاقة لجعلها قابلة للضغط
            if st.button(f"Explore {p['name']}", key=f"btn_{p['name']}", use_container_width=True):
                st.session_state.selected_platform = p['name']
                st.session_state.current_page = 'products'
                st.rerun()

# ==========================================
# صفحة عرض المنتجات (بعد اختيار المنصة)
# ==========================================
elif st.session_state.current_page == 'products':
    
    # زر العودة
    if st.button("← Back to Platforms"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='font-family: \"Playfair Display\", serif; color: #fff;'>{st.session_state.selected_platform} — <span style='color:#d4af37;'>Trending Products</span></h2>", unsafe_allow_html=True)
    st.write("TOP PRODUCTS · RANKED BY AI TREND ANALYSIS")
    st.write("---")
    
    # رسالة مؤقتة لتوضيح أننا في قسم المنتجات
    st.info(f"You are now exploring live trends on **{st.session_state.selected_platform}**. The product grid and AI brand generation features will be connected to the API in the next step.")