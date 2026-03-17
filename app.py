import streamlit as st
import google.generativeai as genai
import os

# إعدادات الصفحة
st.set_page_config(page_title="WAFEEQ AI", layout="wide")

# الربط بالمفتاح من الخزنة
if "GOOGLE_API_KEY" in st.secrets:
    # الطريقة الحديثة للربط
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing GOOGLE_API_KEY in Secrets!")
    st.stop()

st.markdown("<h1 style='text-align:center; color:#d4af37;'>WAFEEQ AI</h1>", unsafe_allow_html=True)
st.write("---")

# وظيفة توليد النص مع معالجة الأخطاء الذكية
def generate_luxury_brand(product_name):
    try:
        # استخدام الموديل المستقر
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Give me one luxury brand name for {product_name}. One word only.")
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

col1, col2 = st.columns(2)

with col1:
    st.image("https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600", caption="Luxury Watch")
    if st.button("✨ Generate Brand Name", key="watch_btn"):
        with st.spinner("Connecting to Google AI..."):
            result = generate_luxury_brand("Luxury Watch")
            if "Error" in result:
                st.error(result)
            else:
                st.balloons()
                st.success(f"Recommended Brand: {result}")

with col2:
    st.image("https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600", caption="Leather Bag")
    if st.button("✨ Generate Luxury Tagline", key="bag_btn"):
        with st.spinner("Analyzing..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content("Give me one short luxury tagline for a premium bag.")
                st.success(f"Tagline: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")