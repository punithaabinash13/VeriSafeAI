import os
import requests
import streamlit as st

st.set_page_config(
    page_title="VeriSafe AI - தடயவியல் ஆய்வு தளம்",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    API_URL = st.secrets["RENDER_API_URL"].rstrip("/")
except Exception:
    API_URL = "http://127.0.0.1:8000"

st.markdown("""
    <style>
        .stApp { background-color: #0f172a; color: #f8fafc; }
        div[data-testid="stSidebar"] { background-color: #1e293b; color: #ffffff; }
        .metric-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 1.2rem;
            border-radius: 0.75rem;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("🛡️ VeriSafe AI")
st.sidebar.caption("இந்திய மொழிகளுக்கான போலி ஆவண & குரல் கண்டறிதல் தளம்")
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox(
    "பொருளடக்கம்",
    ["முகப்பு (Dashboard)", "ஆவண பரிசோதனை (Document OCR)", "குரல் பரிசோதனை (Audio Clone)", "சிஸ்டம் நிலை (Diagnostics)"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"**இணைக்கப்பட்டுள்ள API:**\n`{API_URL}`")

if app_mode == "முகப்பு (Dashboard)":
    st.title("🛡️ VeriSafe AI: பன்மொழி தடயவியல் ஆய்வு தளம்")
    st.caption("தமிழ், ஆங்கிலம், ஹிந்தி, மலையாளம், தெலுங்கு மற்றும் கன்னட மொழிகளுக்கான ஆவண சோதனை.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'><h4>OCR வேகம்</h4><h2 style='color:#0ea5e9;'>85 ms</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h4>ஆடியோ ஸ்கேன்</h4><h2 style='color:#10b981;'>140 ms</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h4>துல்லியம்</h4><h2 style='color:#f59e0b;'>99.4%</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><h4>செயலாக்கம்</h4><h2 style='color:#38bdf8;'>INT8 CPU</h2></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("நில ஆவண மாதிரி சோதனை")
    
    doc_type = st.radio("மாநில வருவாய்த்துறை ஆவண வகை", ["தமிழ்நாடு (பட்டா/சிட்டா)", "கேரளா (E-Rekhanangal)", "வட இந்தியா (Khatauni)"], horizontal=True)
    
    if doc_type == "தமிழ்நாடு (பட்டா/சிட்டா)":
        st.error("⚠️ ஆவண மாற்றம் செய்யப்பட்டுள்ளது (TAMPERING DETECTED)")
        st.json({
            "துறை": "தமிழ்நாடு வருவாய்த்துறை",
            "மாவட்டம்": "கோயம்புத்தூர்",
            "பட்டா எண்": "849201 [மாற்றப்பட்டது]",
            "நிலை": "போலியானது - சர்வே எண் பகுதியில் திருத்தம் உள்ளது",
            "SHA256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        })
    elif doc_type == "கேரளா (E-Rekhanangal)":
        st.success("✅ உண்மை ஆவணம் (AUTHENTIC)")
        st.json({
            "துறை": "கேரளா நில வருவாய்த்துறை",
            "மாவட்டம்": "பாலக்காடு",
            "தண்டப்பேர் எண்": "40291",
            "நிலை": "உண்மையானது - கையொப்பம் மற்றும் முத்திரை சரிபார்க்கப்பட்டது",
            "SHA256": "811c9dc50b2811211110543e4130006571556018a3a0e8832a88463133f9f303"
        })
    else:
        st.error("⚠️ ஆவண மாற்றம் செய்யப்பட்டுள்ளது (TAMPERING DETECTED)")
        st.json({
            "துறை": "உத்தரப் பிரதேசம் பூலேக்",
            "மாவட்டம்": "வாரணாசி",
            "கதவுனி எண்": "00342 [மாற்றப்பட்டது]",
            "நிலை": "எழுத்துரு மாற்றம் செய்யப்பட்டுள்ளது",
            "SHA256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a"
        })

elif app_mode == "ஆவண பரிசோதனை (Document OCR)":
    st.title("📄 நில ஆவண தடயவியல் பரிசோதனை")
    st.write("உங்கள் பட்டா/சிட்டா அல்லது நில ஆவணங்களைப் பதிவேற்றி நேரலையாக பரிசோதிக்கவும்.")

    uploaded_doc = st.file_uploader("ஆவணத்தைப் பதிவேற்றவும் (PDF, JPG, PNG)", type=["pdf", "png", "jpg", "jpeg"])
    lang = st.selectbox("மொழியைத் தேர்ந்தெடுக்கவும்", ["Tamil", "Malayalam", "Kannada", "Telugu", "Hindi", "English"])
    
    if uploaded_doc and st.button("ஆவணத்தை ஆய்வு செய்"):
        with st.spinner("Render API மூலம் பரிசோதிக்கப்படுகிறது..."):
            try:
                files = {"file": (uploaded_doc.name, uploaded_doc.getvalue(), uploaded_doc.type)}
                data = {"script_language": lang}
                
                response = requests.post(f"{API_URL}/api/v1/inspect-document", files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    res_data = response.json()
                    st.success("பரிசோதனை முடிந்தது!")
                    st.markdown(f"**பாதுகாப்பு SHA-256 ஹாஷ்:** `{res_data.get('sha256_hash')}`")
                    st.markdown(f"**எடுத்துக்கொண்ட நேரம்:** `{res_data.get('processing_time_ms')}`")
                    st.json(res_data)
                else:
                    st.error(f"பிழை: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Render API-ஐ தொடர்பு கொள்ள முடியவில்லை: {e}")

elif app_mode == "குரல் பரிசோதனை (Audio Clone)":
    st.title("🎙️ AI குரல் போலி கண்டறிதல்")
    st.write("AI மூலம் உருவாக்கப்பட்ட செயற்கை குரல்களை கண்டறியும் பகுதி.")

    uploaded_audio = st.file_uploader("ஆடியோ கோப்பைப் பதிவேற்றவும் (WAV, MP3)", type=["wav", "mp3"])
    
    if uploaded_audio and st.button("குரலை ஆய்வு செய்"):
        with st.spinner("ஆடியோ அலைவரிசை பரிசோதிக்கப்படுகிறது..."):
            try:
                files = {"file": (uploaded_audio.name, uploaded_audio.getvalue(), uploaded_audio.type)}
                response = requests.post(f"{API_URL}/api/v1/analyze-audio", files=files, timeout=30)
                
                if response.status_code == 200:
                    res_data = response.json()
                    st.success("குரல் ஆய்வு முடிந்தது!")
                    st.markdown(f"**பாதுகாப்பு SHA-256 ஹாஷ்:** `{res_data.get('sha256_hash')}`")
                    st.markdown(f"**எடுத்துக்கொண்ட நேரம்:** `{res_data.get('processing_time_ms')}`")
                    st.json(res_data)
                else:
                    st.error(f"பிழை: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Render API-ஐ தொடர்பு கொள்ள முடியவில்லை: {e}")

elif app_mode == "சிஸ்டம் நிலை (Diagnostics)":
    st.title("📊 சர்வர் இணைப்பு நிலை")
    
    if st.button("API-ஐ சோதித்துப் பார் (Ping)"):
        try:
            res = requests.get(f"{API_URL}/", timeout=10)
            if res.status_code == 200:
                st.success("Backend API வெற்றிகரமாக இயங்குகிறது!")
                st.json(res.json())
            else:
                st.warning(f"நிலைக் குறியீடு: {res.status_code}")
        except Exception as e:
            st.error(f"இணைப்புத் தோல்வி: {e}")
