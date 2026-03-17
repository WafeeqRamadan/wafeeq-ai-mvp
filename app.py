import streamlit as st
import google.generativeai as genai
import time

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(
    page_title="WAFEEQ AI - Founder's Radar",
    page_icon="🚀",
    layout="wide", # جعل الواجهة عريضة لتستوعب البطاقات
    initial_sidebar_state="collapsed"
)

# --- 2. الخزنة السرية للمفتاح (تأكد من وضع مفتاحك الحقيقي في إعدادات Streamlit) ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing Google API Key. Please add it to Streamlit Secrets.")
    st.stop()
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 3. محرك الـ AI (إصدار Gemini 1.5 PRO) ---
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 4. CSS المتقدم لتحويل الواجهة إلى "فخمة" (التحول الجذري) ---
hide_st_style = """
<style>
/* استيراد خط Poppins العصري */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* تطبيق الخط والخلفية السوداء العميقة على التطبيق بالكامل */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Poppins', sans-serif;
    background-color: #050509; /* أسود أعمق وفخم */
    color: #ffffff;
}

/* إخفاء عناصر Streamlit الافتراضية تماماً */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stHeader"] {background: rgba(0,0,0,0);} /* إخفاء الهيدر الشفاف */
[class^="viewerBadge_"] {display: none !important;} /* إخفاء العلامة المائية */

/* تنسيق العنوان الرئيسي بتأثير التوهج (Neon Glow) */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 15px rgba(79, 172, 254, 0.5);
}

.sub-title {
    font-size: 1.2rem;
    text-align: center;
    color: #a0a0a0;
    margin-bottom: 3rem;
    font-weight: 300;
}

/* تصميم بطاقات المنتجات (Product Cards) مستوحاة من أمثلتك */
.product-card {
    background-color: #11112d; /* رمادي مزرق غامق للبطاقة */
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid #1f1f3e;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* تأثير التوهج عند تمرير الماوس على البطاقة */
.product-card:hover {
    transform: translateY(-5px);
    border-color: #4facfe;
    box-shadow: 0 10px 20px rgba(79, 172, 254, 0.2);
}

.product-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 15px;
}

.product-name {
    font-size: 1.4rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 5px;
}

.product-category {
    font-size: 0.9rem;
    color: #00f2fe; /* لون سماوي فخم للتصنيف */
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.product-price {
    font-size: 1.2rem;
    font-weight: 700;
    color: #4facfe;
    margin-bottom: 15px;
}

/* تنسيق الأزرار الافتراضية لتصبح " Glowing Neon" */
div.stButton > button {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
    color: #050509 !important;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    box-shadow: 0 0 15px rgba(79, 172, 254, 0.8);
    transform: scale(1.03);
}

div.stButton > button:active {
    transform: scale(0.98);
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 5. محتوى الصفحة الرئيسية ---
st.markdown('<div class="main-title">WAFEEQ AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Founder\'s High-Potential Product Radar</div>', unsafe_allow_html=True)

# بيانات المنتجات (الرادار) - نفس البيانات ولكن سنعرضها كبطاقات
products = [
    {
        "name": "Blink Mini Pan-Tilt Camera",
        "category": "Home Security",
        "price": "$29.99",
        "image": "https://m.media-amazon.com/images/I/51gI-5r+hHL._AC_UL400_.jpg"
    },
    {
        "name": "Portable Blender for Shakes",
        "category": "Kitchen Appliances",
        "price": "$35.99",
        "image": "https://m.media-amazon.com/images/I/7 + bW5X8HwL._AC_UL400_.jpg"
    },
    {
        "name": "Self-Cleaning Cat Litter Box",
        "category": "Pet Supplies",
        "price": "$499.00",
        "image": "https://m.media-amazon.com/images/I/71x4x7V + cPL._AC_UL400_.jpg"
    },
     {
        "name": "Professional Espresso Machine",
        "category": "Appliances",
        "price": "$599.99",
        "image": "https://m.media-amazon.com/images/I/71X1p5N + bPL._AC_UL400_.jpg"
    }
]

# --- 6. عرض المنتجات في "بطاقات" (Cards) فخمة بدلاً من الجدول ---
st.markdown("### 📡 Live Radar: High-Potential Products")

# تقسيم الصفحة إلى 4 أعمدة لعرض البطاقات بجوار بعضها
cols = st.columns(4)

for i, product in enumerate(products):
    with cols[i % 4]:
        # إنشاء هيكل البطاقة باستخدام HTML/CSS داخل st.markdown
        card_html = f"""
        <div class="product-card">
            <img src="{product['image']}" class="product-image" alt="{product['name']}">
            <div class="product-category">{product['category']}</div>
            <div class="product-name">{product['name']}</div>
            <div class="product-price">{product['price']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # إضافة الزر التفاعلي أسفل كل بطاقة
        button_key = f"init_{i}"
        if st.button(f"🚀 Initialize {product['name']}", key=button_key):
            st.warning(f"Feature under development. Contact COO for beta access.")

# --- 7. قسم التحليل (سيظهر عند الضغط على الزر) ---
st.write("---")
# (باقي كود التحليل يمكن إضافته هنا لاحقاً)