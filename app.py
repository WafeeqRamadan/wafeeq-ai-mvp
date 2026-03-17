import streamlit as st
import google.generativeai as genai
import time

# ==========================================
# 1. الإعدادات الأساسية
# ==========================================
st.set_page_config(
    page_title="WAFEEQ AI | E-Commerce Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. الخزنة السرية للمفتاح 
# ==========================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing Google API Key. Please add it to Streamlit Secrets.")
    st.stop()
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-pro')

# ==========================================
# 3. CSS المتقدم: الفخامة والذهبي (Luxury UI)
# ==========================================
luxury_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700&display=swap');

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
    font-size: 4.5rem;
    font-weight: 400;
    text-align: center;
    color: #ffffff;
    line-height: 1.2;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.hero-title span {
    color: #d4af37;
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

/* تنسيق حقول الإدخال */
.stTextInput input {
    background-color: #121212;
    color: #fff;
    border: 1px solid #d4af37;
    border-radius: 4px;
}
</style>
"""
st.markdown(luxury_css, unsafe_allow_html=True)

# ==========================================
# 4. إدارة حالة التطبيق (Navigation)
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = 'Amazon'

st.markdown("""
<div class="top-nav">
    <div class="logo-text">WAFEEQ <span>AI</span></div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. قاعدة بيانات المنتجات الديناميكية
# ==========================================
# هذه البيانات تتغير حسب السوق المختار لإعطاء شعور بالاحترافية
db_products = {
    "Amazon": [
        {"id": "a1", "name": "Chronograph Elite Watch", "category": "ACCESSORIES", "score": "↗ 97", "price": "$249.99", "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "a2", "name": "Minimalist Leather Tote", "category": "FASHION", "score": "↗ 94", "price": "$189.00", "image": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "a3", "name": "Wireless ANC Earbuds", "category": "ELECTRONICS", "score": "↗ 91", "price": "$159.99", "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "a4", "name": "Smart Home Espresso Maker", "category": "APPLIANCES", "score": "↗ 89", "price": "$399.00", "image": "https://images.unsplash.com/photo-1517246286411-8bb31bf4148b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "a5", "name": "Ergonomic Office Chair", "category": "FURNITURE", "score": "↗ 88", "price": "$299.99", "image": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "a6", "name": "Ceramic Matcha Set", "category": "HOME & KITCHEN", "score": "↗ 85", "price": "$45.00", "image": "https://images.unsplash.com/photo-1582793988951-9aed550cbe14?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"}
    ],
    "TikTok Shop": [
        {"id": "t1", "name": "LED Vanity Mirror", "category": "BEAUTY", "score": "↗ 99", "price": "$35.00", "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "t2", "name": "Cloud Slippers", "category": "FASHION", "score": "↗ 98", "price": "$24.99", "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "t3", "name": "Heatless Hair Curler", "category": "BEAUTY", "score": "↗ 95", "price": "$15.99", "image": "https://images.unsplash.com/photo-1522337660859-02fbefca4702?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "t4", "name": "Sunset Projection Lamp", "category": "DECOR", "score": "↗ 93", "price": "$19.99", "image": "https://images.unsplash.com/photo-1565814329452-e1efa11c5e8d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"}
    ],
    "AliExpress": [
        {"id": "al1", "name": "Mini Projector 4K", "category": "TECH", "score": "↗ 96", "price": "$65.00", "image": "https://images.unsplash.com/photo-1585862705626-880053916960?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "al2", "name": "Mechanical Keyboard", "category": "GAMING", "score": "↗ 92", "price": "$45.99", "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"},
        {"id": "al3", "name": "Carpet Cleaning Brush", "category": "HOME", "score": "↗ 89", "price": "$12.50", "image": "https://images.unsplash.com/photo-1585421514284-ceb93e8784ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"}
    ]
}

# ==========================================
# الصفحة الرئيسية (Landing Page)
# ==========================================
if st.session_state.current_page == 'home':
    
    st.markdown("""
    <div class="hero-title">Discover Trending Products<br>Across <span>Every Platform</span></div>
    <div class="hero-subtitle">Real-time trend analysis and luxury brand content generation for the world's top e-commerce marketplaces. From product discovery to branded launch — in one click.</div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("<h3 style='text-align: center; font-family: \"Playfair Display\", serif; font-weight: 400; color: #fff; margin-bottom: 2rem;'>Choose Your <span style='color:#d4af37; font-style:italic;'>Platform</span></h3>", unsafe_allow_html=True)
    
    platforms = [
        {"icon": "A", "name": "Amazon", "desc": "World's largest e-commerce marketplace", "stats": "2.4M+ products"},
        {"icon": "AE", "name": "AliExpress", "desc": "Direct suppliers from global manufacturers", "stats": "1.8M+ products"},
        {"icon": "TT", "name": "TikTok Shop", "desc": "Viral product discovery for Gen Z & beyond", "stats": "980K+ products"},
        {"icon": "W", "name": "Walmart", "desc": "Dominant US retail marketplace", "stats": "1.2M+ products"},
        {"icon": "Et", "name": "Etsy", "desc": "Handmade, vintage & unique products", "stats": "650K+ products"},
        {"icon": "eB", "name": "eBay", "desc": "Auctions, collectibles & direct sales", "stats": "1.5M+ products"}
    ]
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3]
    
    for i, p in enumerate(platforms):
        with cols[i]:
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
            if st.button(f"Explore {p['name']}", key=f"btn_{p['name']}", use_container_width=True):
                st.session_state.selected_platform = p['name']
                st.session_state.current_page = 'products'
                st.rerun()

# ==========================================
# صفحة عرض المنتجات والذكاء الاصطناعي
# ==========================================
elif st.session_state.current_page == 'products':
    
    if st.button("← Back to Platforms"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='font-family: \"Playfair Display\", serif; color: #fff;'>{st.session_state.selected_platform} — <span style='color:#d4af37;'>Trending Products</span></h2>", unsafe_allow_html=True)
    st.write("TOP PRODUCTS · RANKED BY AI TREND ANALYSIS")
    
    # ميزة "رادار النيتش" للبحث المخصص
    with st.expander("🔍 Can't find what you want? Search a specific niche"):
        niche_query = st.text_input("Enter a niche (e.g., Pet Toys, Smart Home, Fitness):")
        if st.button("Scan Niche Trends"):
            if niche_query:
                st.info(f"AI Radar is actively scanning '{niche_query}' trends on {st.session_state.selected_platform}... (API Integration Pending in v2.0)")
    
    st.write("---")
    
    # جلب المنتجات الخاصة بالمنصة المختارة (وإذا لم تكن في الداتا نعرض أمازون كافتراضي)
    current_products = db_products.get(st.session_state.selected_platform, db_products["Amazon"])
    
    # عرض كل المنتجات في شبكة من 3 أعمدة
    cols = st.columns(3)
    
    for i, prod in enumerate(current_products):
        with cols[i % 3]:
            card = f"""
            <div class="platform-card" style="padding: 15px; margin-bottom: 20px;">
                <img src="{prod['image']}" style="width:100%; height:200px; object-fit:cover; border-radius:8px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; color:#888; font-size:0.8rem; margin-bottom:10px;">
                    <span>{prod['category']}</span>
                    <span style="color:#d4af37; border: 1px solid #d4af37; padding: 2px 6px; border-radius: 4px;">{prod['score']}</span>
                </div>
                <h3 style="margin:0 0 10px 0; font-size:1.2rem; color:#fff;">{prod['name']}</h3>
                <div style="color:#d4af37; font-family:'Playfair Display', serif; font-size:1.3rem; margin-bottom:15px;">{prod['price']}</div>
            </div>
            """
            st.markdown(card, unsafe_allow_html=True)
            
            # الزر الذهبي للذكاء الاصطناعي
            if st.button(f"✨ Generate Luxury Brand", key=f"gen_{prod['id']}"):
                with st.spinner('AI is crafting your luxury brand strategy...'):
                    prompt = f"""
                    You are a world-class luxury brand strategist. I have a trending e-commerce product: "{prod['name']}".
                    Create a luxury brand identity for this product to sell it at a premium price.
                    
                    Format your response strictly as follows:
                    **Brand Name:** [Invent a short, elegant, premium name]
                    **Tagline:** [One short, luxurious sentence]
                    **Target Audience:** [Who buys this premium product?]
                    **Luxury Marketing Copy:** [A 3-sentence emotional, high-end description to use on the website]
                    """
                    try:
                        response = model.generate_content(prompt)
                        st.session_state[f"result_{prod['id']}"] = response.text
                    except Exception as e:
                        st.error("Error communicating with AI. Check your API key.")
            
            # إظهار النتيجة تحت المنتج
            if f"result_{prod['id']}" in st.session_state:
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✨ Brand Generated!")
                with st.expander("View Brand Strategy", expanded=True):
                    st.write(st.session_state[f"result_{prod['id']}"])