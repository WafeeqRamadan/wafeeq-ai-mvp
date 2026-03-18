import streamlit as st
import requests

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | Luxury Intelligence", page_icon="✨", layout="wide")

# ==========================================
# 2. إعداد المفتاح السري
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري (GOOGLE_API_KEY) في الخزنة.")
    st.stop()

# ==========================================
# 3. العقل المدبر (الكود ذاتي العلاج لاكتشاف الموديلات)
# ==========================================
def generate_brand_smart(prompt):
    # الخطوة 1: سؤال جوجل عن الموديلات المسموحة لهذا المفتاح
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        res = requests.get(list_url)
        if res.status_code != 200:
            return f"❌ خطأ في المفتاح: {res.text}"
            
        models = res.json().get('models', [])
        working_model = None
        
        # البحث عن أول موديل مسموح له بالكتابة (generateContent)
        for m in models:
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                working_model = m['name'] # سيلتقط الاسم الصحيح أياً كان (gemini-pro, gemini-1.5 الخ)
                if 'gemini-1.5' in working_model: 
                    break # إذا وجد الأحدث، يتوقف
        
        if not working_model:
            return "❌ لم نعثر على أي موديل متاح لهذا المفتاح! يرجى عمل مفتاح جديد."

        # الخطوة 2: إرسال الطلب للموديل الذي تم اكتشافه
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{working_model}:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        
        gen_res = requests.post(gen_url, headers=headers, json=payload)
        
        if gen_res.status_code == 200:
            return gen_res.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ خطأ أثناء التوليد: {gen_res.text}"
            
    except Exception as e:
        return f"❌ عطل في الشبكة: {str(e)}"

# ==========================================
# 4. التصميم الفاخر (CSS)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Lato', sans-serif; }
#MainMenu, footer, header, [data-testid="stDecoration"], [class^="viewerBadge_"] { display: none !important; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3.5rem; text-align: center; color: #ffffff; margin-top: 1rem; margin-bottom: 2rem;}
.hero-title span { color: #d4af37; font-style: italic; }

.platform-card { background-color: #0f0f0f; border: 1px solid #1a1a1a; border-radius: 12px; padding: 25px; transition: 0.3s; text-align: center; height: 100%;}
.platform-card:hover { border-color: #d4af37; background-color: #121212; transform: translateY(-5px); }
.platform-icon { font-size: 2.5rem; color: #d4af37; margin-bottom: 15px; }
.platform-name { font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 10px;}

div.stButton > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border: none; border-radius: 4px; width: 100%; padding: 12px; transition: 0.3s; margin-top: 10px;}
div.stButton > button:hover { background-color: #fff; box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px 0; border-bottom: 1px solid #222; margin-bottom: 2rem;}
.logo-text span { color: #d4af37; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. محرك التطبيق والواجهة
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

db = {
    "Amazon": [
        {"name": "Minimalist Ceramic Watch", "price": "$120", "score": "97", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"},
        {"name": "Handcrafted Leather Bag", "price": "$250", "score": "94", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600"}
    ]
}

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
                with st.spinner("AI is bypassing servers and crafting strategy..."):
                    prompt = f"Act as a high-end luxury brand strategist. Suggest an elegant brand name and a short premium tagline for: {item['name']}."
                    result = generate_brand_smart(prompt)
                    
                    if "❌" in result:
                        st.error(result)
                    else:
                        st.session_state[f"res_{i}"] = result
                        st.balloons()
            
            if f"res_{i}" in st.session_state:
                st.markdown(f"<div style='background-color:#111; padding:20px; border-radius:8px; border-left:4px solid #d4af37; margin-top:15px; color:#ddd;'>{st.session_state[f'res_{i}']}</div>", unsafe_allow_html=True)