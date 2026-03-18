import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | Luxury Intelligence", page_icon="✨", layout="wide")

# ==========================================
# 2. إعدادات الذكاء الاصطناعي (أحدث إصدار)
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # الموديل الأسرع والأكثر استقراراً
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري (GOOGLE_API_KEY) في الخزنة.")
    st.stop()

# ==========================================
# 3. التصميم الفاخر (CSS)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Lato', sans-serif; }
#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] { display: none !important; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3.5rem; text-align: center; color: #ffffff; margin-top: 2rem; margin-bottom: 2rem;}
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card { background-color: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 12px; padding: 25px; transition: 0.3s; text-align: center; height: 100%;}
.platform-card:hover { border-color: #d4af37; background-color: #121212; transform: translateY(-5px); }
.platform-icon { font-size: 2.5rem; color: #d4af37; margin-bottom: 15px; }
.platform-name { font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 10px;}
.platform-stats { color: #888; font-size: 0.9rem; }

div.stButton > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border: none; border-radius: 4px; width: 100%; padding: 12px; transition: 0.3s; margin-top: 10px;}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px 0; border-bottom: 1px solid #222; margin-bottom: 2rem;}
.logo-text span { color: #d4af37; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. محرك التطبيق (البيانات والتنقل)
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

# قاعدة بيانات المنتجات للمعاينة
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
    platforms = [
        ("fa-brands fa-amazon", "Amazon", "2.4M+ Items"), 
        ("fa-brands fa-tiktok", "TikTok Shop", "980K+ Items"), 
        ("fa-solid fa-cart-shopping", "AliExpress", "1.8M+ Items")
    ]
    
    for i, (icon, name, stats) in enumerate(platforms):
        with cols[i]:
            st.markdown(f'<div class="platform-card"><div class="platform-icon"><i class="{icon}"></i></div><div class="platform-name">{name}</div><div class="platform-stats">{stats}</div></div>', unsafe_allow_html=True)
            if st.button(f"Explore {name}", key=f"p_{i}"):
                st.session_state.platform = name
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة المنتجات وتوليد البراند ---
elif st.session_state.page == 'details':
    if st.button("← Back to Platforms"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2>{st.session_state.platform} <span style='color:#d4af37;'>Trending Radar</span></h2>", unsafe_allow_html=True)
    st.write("---")
    
    items = db.get(st.session_state.platform, db["Amazon"]) # افتراضياً نعرض أمازون كنموذج
    cols = st.columns(2)
    
    for i, item in enumerate(items):
        with cols[i]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"<h3 style='margin-top:15px;'>{item['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span style='color:#d4af37; font-weight:bold; font-size:1.2rem;'>{item['price']}</span> | Trend Score: {item['score']}", unsafe_allow_html=True)
            
            if st.button(f"✨ Build Brand Strategy", key=f"btn_{i}"):
                with st.spinner("AI is crafting your luxury strategy..."):
                    try:
                        prompt = f"Act as a high-end luxury brand strategist. Suggest an elegant brand name and a short premium tagline for: {item['name']}."
                        response = model.generate_content(prompt)
                        st.session_state[f"res_{i}"] = response.text
                        st.balloons()
                    except Exception as e:
                        st.error(f"⚠️ حدث خطأ في الاتصال: {e}")
            
            if f"res_{i}" in st.session_state:
                st.markdown(f"<div style='background-color:#111; padding:20px; border-radius:8px; border-left:4px solid #d4af37; margin-top:15px; color:#ddd;'>{st.session_state[f'res_{i}']}</div>", unsafe_allow_html=True)