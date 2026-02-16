import streamlit as st
import joblib
import numpy as np
import random
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="SecurePay AI",
    page_icon="🛡️",
    layout="wide"
)

# --- Professional Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #1e40af !important;
        font-family: 'Inter', sans-serif;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        margin: 20px 0;
    }
    .fraud-box {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 2px solid #ef4444;
    }
    .safe-box {
        background-color: #dcfce7;
        color: #15803d;
        border: 2px solid #22c55e;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Model Loading (Fixed Permission Error) ---
@st.cache_resource
def load_model_file():
    model_name = 'trained model .pkl'
    # Define absolute paths to the FILE, not the folder
    paths = [
        os.path.join(os.path.dirname(__file__), model_name),
        os.path.join(r"C:\Users\SPARTA\Desktop\Fraud Detection system", model_name)
    ]
    
    for path in paths:
        if os.path.isfile(path): # Checks if it's a file, prevents directory error
            try:
                return joblib.load(path)
            except Exception as e:
                st.sidebar.error(f"Load error: {e}")
    return None

model = load_model_file()

# --- Session State Management ---
if 'captcha' not in st.session_state:
    st.session_state.captcha = str(random.randint(1000, 9999))

# --- Sidebar UI ---
with st.sidebar:
    st.title("🛡️ SecurePay AI")
    st.subheader("System Status")
    st.divider()
    
    if model:
        st.success("Core Engine: ONLINE")
    else:
        st.error("Core Engine: OFFLINE")
        st.info("Check if 'securepay_model.pkl' is in the project folder.")
    
    if st.button("Regenerate Security Code"):
        st.session_state.captcha = str(random.randint(1000, 9999))
        st.rerun()

# --- Main Interface ---
st.title("Credit Card Fraud Analysis")
st.write("Enterprise-grade transaction monitoring and risk assessment.")

if model is None:
    st.error("🚨 **System Critical:** Model file not detected. Analysis features are disabled.")
else:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="card"><h3>Transaction Details</h3>', unsafe_allow_html=True)
        amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=100.0, step=0.01)
        tr_time = st.number_input("Time Elapsed (Seconds)", min_value=0.0, value=0.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>Security Check</h3>', unsafe_allow_html=True)
        st.info(f"Security Code: **{st.session_state.captcha}**")
        captcha_input = st.text_input("Enter Code", placeholder="Type code here")
        analyze_btn = st.button("Analyze Transaction")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Prediction Logic ---
    if analyze_btn:
        if captcha_input != st.session_state.captcha:
            st.warning("Verification failed: Incorrect security code.")
        elif amount <= 0:
            st.warning("Please enter a valid amount.")
        else:
            with st.spinner("AI Engine evaluating risk..."):
                time.sleep(1) # Simulated processing
                
                # Prepare input data (Match the 30 features your model expects)
                # Note: This assumes V1-V28 are 0, with Amount and Time at specific indices
                input_data = np.zeros(30)
                input_data[28] = amount
                input_data[29] = tr_time
                
                prediction = model.predict([input_data])
                
                # Logic: Fraud if model says so OR if amount is unrealistically high
                is_fraud = True if (prediction[0] == 1 or amount > 25000) else False
                
                if is_fraud:
                    st.markdown('<div class="result-box fraud-box">🚨 FRAUDULENT TRANSACTION DETECTED</div>', unsafe_allow_html=True)
                    st.error(f"High risk detected for transaction of ${amount:,.2f}. The system has flagged this account.")
                else:
                    st.markdown('<div class="result-box safe-box">✅ TRANSACTION IS SECURE</div>', unsafe_allow_html=True)
                    st.success(f"Transaction of ${amount:,.2f} has been approved successfully.")
                
                # Refresh captcha for next run
                st.session_state.captcha = str(random.randint(1000, 9999))

st.divider()

st.caption("© 2026 SecurePay Technologies | Neural Risk Mitigation v2.4")
