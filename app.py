import streamlit as st
import requests
import json
import urllib.parse

# ==========================================
# 1. الإعدادات الأساسية
# ==========================================
st.set_page_config(page_title="WAFEEQ AI | Live Market Radar", page_icon="📡", layout="wide")

if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ لم يتم العثور على المفتاح السري (GOOGLE_API_KEY) في الخزنة.")
    st.stop()

# ==========================================
# 2. محركات الذكاء الاصطناعي 
# ==========================================
@st.cache_data(ttl=3600)
def get_free_tier_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            models = res.json().get('models', [])
            valid_models = [m['name'] for m in models if 'generateContent' in m.get('supportedGenerationMethods', []) and 'vision' not in m['name'] and 'aqa' not in m['name'] and 'embedding' not in m['name']]
            valid_models.sort(key=lambda x: (0 if 'flash' in x.lower() else 1, x))
            return valid_models
        return []
    except:
        return []

def call_gemini(prompt):
    models = get_free_tier_models()
    if not models: return "Error: No models found."
    for model_name in models:
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts":[{"text": prompt}]}]}
        headers = {'Content-Type': 'application/json'}
        try:
            res = requests.post(gen_url, headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return "Error: Request failed."

# ==========================================
# 3. محرك جلب البيانات الحية 
# ==========================================
def fetch_live_trends(niche, platform):
    prompt = f"""
    Act as an expert e-commerce product researcher. Find 2 currently highly trending and profitable products in the '{niche}' niche on {platform}.
    Return ONLY a valid JSON array. Do not include markdown formatting or backticks. Just the raw JSON.
    Format exactly like this:
    [
      {{"name": "Product 1 Name", "price": "$XX.XX", "score": "98", "keyword": "single word for image search"}},
      {{"name": "Product 2 Name", "price": "$YY.YY", "score": "95", "keyword": "single word for image search"}}
    ]
    """
    response = call_gemini(prompt)
    try:
        clean_json = response.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        return None

# ==========================================
# 4. التصميم الفاخر (CSS المثالي)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

html, body, [data-testid="stAppViewContainer"] { background-color: #050505; color: #e0e0e0; font-family: 'Lato', sans-serif; }
#MainMenu, footer, header { visibility: hidden !important; display: none !important; }
[data-testid="stDecoration"], [class*="viewerBadge"], a[href^="https://streamlit.io/cloud"] { display: none !important; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3rem; text-align: center; color: #ffffff; margin-top: 1rem; margin-bottom: 2rem;}
.hero-title span { color: #d4af37; font-style: italic; }

/* 🎯 السحر هنا: تنسيق نموذج البحث الأصلي لستريمليت ليكون فخماً */
[data-testid="stForm"] { background-color: #0f0f0f; padding: 30px; border-radius: 12px; border: 1px solid #222; margin-bottom: 30px; }

/* تنسيق جميع الأزرار (بما فيها زر البحث) */
div.stButton > button, [data-testid="stFormSubmitButton"] > button { background-color: #d4af37; color: #000 !important; font-weight: 700; border: none; border-radius: 4px; padding: 12px; transition: 0.3s; width: 100%;}
div.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover { background-color: #fff; box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }

.logo-text { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #fff; padding: 10px 0; border-bottom: 1px solid #222; margin-bottom: 2rem;}
.logo-text span { color: #d4af37; }

/* تنسيق حقول الإدخال لتتناغم مع اللون الأسود */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1a1a !important; color: #fff !important; border: 1px solid #333 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. واجهة المستخدم
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'

st.markdown('<div class="logo-text">WAFEEQ <span>AI</span></div>', unsafe_allow_html=True)

# --- صفحة البحث الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-title">Live Trend Radar<br>Across <span>Any Niche</span></div>', unsafe_allow_html=True)
    
    # استخدام