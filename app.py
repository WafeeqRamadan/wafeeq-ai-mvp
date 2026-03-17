import streamlit as st
import google.generativeai as genai
import json

# 1. UI Configuration (Futuristic Luxury)
st.set_page_config(page_title="WAFEEQ AI", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    h1, h2, h3, h4 { color: #D4AF37; font-family: 'Helvetica Neue', sans-serif; }
    .product-card { background-color: #111111; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px; transition: 0.3s; }
    .product-card:hover { border-color: #D4AF37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.2); }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 8px; font-weight: bold; width: 100%; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #F3E5AB; color: black; }
    .metric-box { background-color: #1a1a1a; padding: 15px; border-left: 4px solid #D4AF37; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. API Key Configuration
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("WAFEEQ AI ⚡")
st.markdown("### From Trend to Brand in One Click")
st.markdown("---")

# 3. The Omni-Pulse Radar Engine
@st.cache_data(ttl=3600)
def fetch_trending_products():
    prompt = """
    You are an elite e-commerce intelligence engine. Identify 3 highly trending dropshipping products in the US/UK market right now.
    Output EXACTLY in this JSON format without any markdown, backticks, or extra text:
    [
      {"name": "Product Name", "niche": "Category", "buy_price": 10, "sell_price": 40, "market_gap": "The main problem buyers complain about in current market options"}
    ]
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        return [{"name": "Ultra-Portable Espresso Maker", "niche": "Coffee", "buy_price": 18, "sell_price": 65, "market_gap": "Current models have weak pressure and leak hot water easily."}]

if GOOGLE_API_KEY == "ضع_مفتاح_جوجل_هنا_بدون_مسح_علامات_التنصيص":
    st.warning("Please insert your Google API Key in the code to activate the Radar.")
else:
    st.markdown("### 📡 Omni-Pulse Radar (Live Opportunities)")
    
    with st.spinner("Scanning global markets & tracking trends..."):
        trending_products = fetch_trending_products()

    cols = st.columns(len(trending_products))
    
    # 4. The Hunt (Product Cards)
    for idx, product in enumerate(trending_products):
        with cols[idx]:
            st.markdown(f"""
            <div class="product-card">
                <h3 style="margin-top:0;">{product['name']}</h3>
                <p style="color:#888;">Niche: {product['niche']}</p>
                <p><b>Supplier Cost:</b> ${product['buy_price']} | <b>Selling Price:</b> ${product['sell_price']}</p>
                <p style="color:#ff6b6b; font-size:14px;">⚠️ Market Gap: {product['market_gap']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🚀 Initialize Brand", key=f"btn_{idx}"):
                st.session_state['selected_product'] = product

    # 5. One-Click Execution (Math & Voice)
    if 'selected_product' in st.session_state:
        prod = st.session_state['selected_product']
        st.markdown("---")
        st.markdown(f"## ⚙️ Building the Empire for: {prod['name']}")
        
        col_math, col_voice = st.columns(2)
        
        # Precision Margin Architect
        with col_math:
            st.markdown("### 🧮 Precision Margin Architect")
            shipping = 6.0
            cpa_budget = 15.0
            stripe_fee = (prod['sell_price'] * 0.029) + 0.30
            net_profit = prod['sell_price'] - (prod['buy_price'] + shipping + cpa_budget + stripe_fee)
            
            st.markdown(f"""
            <div class="metric-box">
                <h4>Projected Net Profit: <span style="color: {'#00ff00' if net_profit > 10 else '#ff6b6b'};">${net_profit:.2f}</span></h4>
                <p style="margin:0; font-size: 14px; color: #aaa;">After deducting: Shipping (${shipping}), CPA (${cpa_budget}), Stripe Fees (${stripe_fee:.2f})</p>
            </div>
            """, unsafe_allow_html=True)
            
            if net_profit > 10:
                st.success("Green Light: Excellent profit margin for scaling! 🟢")
            else:
                st.error("Warning: Margin is too tight. Consider raising the selling price. 🔴")

        # Cultural Localization Engine
        with col_voice:
            st.markdown("### 🎙️ Cultural Localization Engine")
            with st.spinner("Crafting high-converting localized ad copy..."):
                ad_prompt = f"""
                Write a short, highly engaging TikTok video script/ad copy in native US English for the product '{prod['name']}'. 
                Focus heavily on solving this specific market gap: '{prod['market_gap']}'. 
                The tone should be luxurious, persuasive, and designed to convert immediately. Do not use generic emojis.
                """
                ad_copy = model.generate_content(ad_prompt).text
                st.info(ad_copy)