import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="WAFEEQ AI", page_icon="✨", layout="wide")

# --- 2. الربط الذكي والآمن ---
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # محاولة الاتصال بالموديل المستقر الأضمن عالمياً
        # جربنا flash و pro، الآن سنستخدم الاسم العام الذي يقبله جوجل في كل الحالات
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
    except Exception as e:
        st.error(f"Initialization Error: {e}")
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

# --- 3. CSS الفخامة ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Lato', sans-serif; }
#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] { display: none !important; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 3rem; text-align: center; color: #fff; margin-top: 1rem; }
.hero-title span { color: #d4af37; font-style: italic; }
div.stButton > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border-radius: 4px; width: 100%; border: none; }
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; }
.logo-text span { color: #d4af37; }
</style>
""", unsafe_allow_html=True)

# --- 4. محرك التطبيق ---
if 'page' not in st.session_state: st.session_state.page = 'home'
st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

db = {
    "Amazon": [
        {"id": "a1", "name": "Minimalist Ceramic Watch", "price": "$120", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"id": "a2", "name": "Handcrafted Leather Bag", "price": "$250", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"}
    ]
}

if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Discover Trending Products Across <span>Every Platform</span></div>', unsafe_allow_html=True)
    if st.button("Explore Amazon"):
        st.session_state.platform = "Amazon"
        st.session_state.page = 'details'
        st.rerun()

elif st.session_state.page == 'details':
    if st.button("← Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    items = db["Amazon"]
    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i]:
            st.image(item['img'], use_container_width=True)
            st.markdown(f"### {item['name']}")
            if st.button(f"✨ Build {item['name']} Brand", key=f"btn_{i}"):
                with st.spinner("AI is thinking..."):
                    try:
                        # طلب مباشر وبسيط جداً بدون تحديد إصدارات API معقدة
                        response = model.generate_content("Give me one luxury brand name for this product: " + item['name'])
                        st.session_state[f"res_{i}"] = response.text
                    except Exception as e:
                        # إذا فشل، سنحاول استدعاء الموديل بطريقة بديلة فوراً
                        st.error(f"Connection Issue. Trying backup method...")
                        try:
                            alt_model = genai.GenerativeModel('gemini-pro')
                            response = alt_model.generate_content("One luxury brand name for: " + item['name'])
                            st.session_state[f"res_{i}"] = response.text
                            st.rerun()
                        except:
                            st.error("Please check your Google AI Dashboard. Your API Key might need to be re-generated.")
            
            if f"res_{i}" in st.session_state:
                st.markdown(f"<div style='background:#111; padding:15px; border-left:4px solid #d4af37; color:#d4af37;'>{st.session_state[f"res_{i}"]}</div>", unsafe_allow_html=True)