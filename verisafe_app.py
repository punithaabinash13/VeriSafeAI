import os
import requests
import streamlit as st

st.set_page_config(
    page_title="VeriSafe AI",
    page_icon="🛡️",
    layout="wide"
)

# Fetch Render API endpoint
BACKEND_URL = os.environ.get("BACKEND_API_URL", "https://verisafeai-1.onrender.com")

st.title("🛡️ VeriSafe AI")
st.markdown("Automated Deepfake Detection & Media Authenticity Scanner")

st.sidebar.header("⚙️ Configuration")
language = st.sidebar.selectbox("Choose Language / மொழி:", ["English", "Tamil (தமிழ்)"])

st.markdown("---")

tab1, tab2 = st.tabs(["🎥 VeriSafe AI Scanner", "📄 System Status"])

with tab1:
    st.subheader("Upload Media for Verification")
    uploaded_file = st.file_uploader("Choose an image file (JPG, PNG, WEBP)...", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Input Image", use_container_width=True)
            
        with col2:
            if st.button("🚀 Run VeriSafe AI Analysis", type="primary", use_container_width=True):
                with st.spinner("Analyzing micro-textures with VeriSafe AI..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{BACKEND_URL}/detect-deepfake", files=files, timeout=30)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            if data["is_deepfake"]:
                                st.error(f"🚨 **Verdict:** {data['verdict']}")
                            else:
                                st.success(f"✅ **Verdict:** {data['verdict']}")
                                
                            m1, m2, m3 = st.columns(3)
                            m1.metric("Liveness Score", data["confidence_score"])
                            m2.metric("Noise Variance", data["laplacian_variance"])
                            m3.metric("Latency", f"{data['latency_ms']} ms")
                            
                            st.subheader("VeriSafe AI Security Hash")
                            st.code(f"SHA-256 Hash: {data['forensic_hash']}")
                        else:
                            st.error(f"Server Error ({response.status_code}): {response.text}")
                    except Exception as err:
                        st.error(f"Connection Error: {str(err)}")

with tab2:
    st.subheader("VeriSafe AI Engine Status")
    st.info(f"Connected Backend Engine: `{BACKEND_URL}`")
    if st.button("Check Server Health"):
        try:
            res = requests.get(f"{BACKEND_URL}/")
            st.json(res.json())
        except Exception as e:
            st.error(f"Could not reach backend: {e}")
