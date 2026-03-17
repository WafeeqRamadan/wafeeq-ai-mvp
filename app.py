import streamlit as st
import google.generativeai as genai

# --- 1. الإعدادات الفاخرة للصفحة ---
st.set_page_config(
    page_title="WAFEEQ AI | Luxury Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. الربط بالخزنة السرية (Secrets) ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    st.error("⚠️ خطأ: المفتاح السري غير موجود في إعدادات Secrets!")
    st.stop()

# --- 3. التصميم الجمالي (Luxury Black & Gold) ---
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
    font-size: 4.5rem;
    text-align: center;
    color: #ffffff;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card {
    background-color: #0f0f0f;
    border: 1px solid #1a1a1a;
    border-radius: 15px;
    padding: 25px;
    transition: 0.4s ease-in-out;
    height: 280px;
    margin-bottom: 20px;
    text-align: left;
}
.platform-card:hover { border-color: #d4af37; background-color: #121212; transform: translateY(-8px); }
.platform-icon { font-size: 2.5rem; color: #d4af37; margin-bottom: 20px; }
.platform-name { font-size: 1.6rem; font-weight: 700; color: #fff; }
.platform-stats { color: #d4af37; font-weight: 700; font-size: 0.85rem; margin-top: 15px; }

div.stButton > button {
    background-color: #d4af37;
    color: #000 !important;
    font-weight: 700;
    font-family: 'Lato', sans-serif;
    border: none;
    border-radius: 4px;
    width: 100%;
    transition: 0.3s;
    padding: 10px;
}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 25px rgba(212, 175, 55, 0.5); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 2rem; color: #fff; padding: 15px; }
.logo-text span { color: #d4af37; }
</style>
"""
st.markdown(luxury_style, unsafe_allow_html=True)

# --- 4. محرك البيانات والحالة ---
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

# قاعدة بيانات المنتجات لكل المنصات (أكثر مبيعاً)
db = {
    "Amazon": [
        {"id": "a1", "name": "Minimalist Ceramic Watch", "price": "$120", "trend": "↗ 97", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"id": "a2", "name": "Handcrafted Leather Bag", "price": "$250", "trend": "↗ 94", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"},
        {"id": "a3", "name": "Pro Noise Cancelling Buds", "price": "$199", "trend": "↗ 91", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600"},
        {"id": "a4", "name": "Smart Espresso Station", "price": "$450", "trend": "↗ 89", "img": "https://images.unsplash.com/photo-1517246286411-8bb31bf4148b?w=600"}
    ],
    "TikTok Shop": [
        {"id": "t1", "name": "Sunset Atmosphere Lamp", "price": "$29", "trend": "↗ 99", "img": "https://images.unsplash.com/photo-1565814329452-e1efa11c5e8d?w=600"},
        {"id": "t2", "name": "Ergonomic Cloud Slippers", "price": "$22", "trend": "↗ 98", "img": "https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=600"},
        {"id": "t3", "name": "Mini Portable Projector", "price": "$85", "trend": "↗ 95", "img": "https://images.unsplash.com/photo-1585862705626-880053916960?w=600"}
    ],
    "AliExpress": [
        {"id": "al1", "name": "Retro Mechanical Keyboard", "price": "$55", "trend": "↗ 96", "img": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600"},
        {"id": "al2", "name": "Smart Pet Feeder 4L", "price": "$78", "trend": "↗ 92", "img": "https://images.unsplash.com/photo-1582793988951-9aed550cbe14?w=600"}
    ]
}

# --- صفحة الهبوط ---
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
            if st.button(f"Explore {p['name']}", key=f"p_btn_{i}"):
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
            st.markdown(f"<span style='color:#d4af37; font-weight:bold;'>{item['price']}</span> | Trend Score: {item['trend']}", unsafe_allow_html=True)
            
            if st.button(f"✨ Build {item['name']} Brand", key=f"gen_btn_{i}"):
                with st.spinner("AI Strategy in progress..."):
                    try:
                        prompt = f"As a luxury brand expert, create an elegant brand name, a poetic tagline, and a 2-sentence high-end sales pitch for: {item['name']}. Focus on wealth, exclusivity, and quality."
                        response = model.generate_content(prompt)
                        st.session_state[f"res_{i}"] = response.text
                    except Exception as e:
                        st.error("خطأ في الاتصال بالذكاء الاصطناعي! تأكد من صحة مفتاح الـ API في الإعدادات.")
            
            if f"res_{i}" in st.session_state:
                st.markdown("---")
                st.info(st.session_state[f"res_{i}"])