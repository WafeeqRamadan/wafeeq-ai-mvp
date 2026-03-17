import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="WAFEEQ AI", layout="wide")

# الربط بالمفتاح
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام الموديل الأكثر استقراراً وبساطة
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

# تصميم بسيط وفخم
st.markdown("<h1 style='text-align:center; color:#d4af37;'>WAFEEQ AI</h1>", unsafe_allow_html=True)
st.write("---")

# تجربة المنتج
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600", caption="Luxury Watch")
    if st.button("✨ Generate Brand Name"):
        try:
            # محاولة توليد نص بسيط جداً
            response = model.generate_content("Give me one luxury brand name for a watch. One word only.")
            st.success(f"Brand Name: {response.text}")
        except Exception as e:
            st.error(f"Google AI Error: {e}")
            st.info("If you see 404, your API Key is not for Gemini. Please create a NEW key from Google AI Studio.")

with col2:
    st.image("https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600", caption="Leather Bag")
    if st.button("✨ Generate Tagline"):
        try:
            response = model.generate_content("Give me one luxury tagline for a bag.")
            st.success(f"Tagline: {response.text}")
        except Exception as e:
            st.error(f"Google AI Error: {e}")