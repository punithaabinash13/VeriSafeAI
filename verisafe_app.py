import os
import requests
import streamlit as st

st.set_page_config(page_title="VeriSafe AI", page_icon="🛡️", layout="wide")

BACKEND_URL = os.environ.get("BACKEND_API_URL", "https://verisafeai-1.onrender.com")

I18N = {
    "English": {
        "title": "🛡️ VeriSafe AI",
        "subtitle": "Multi-Modal Deepfake & Document Fraud Detection Platform (94.4% Accuracy)",
        "tabs": ["📷 Photo Analysis", "🎥 Video Analysis", "🎙️ Audio Analysis", "📄 Document Verification"],
        "upload": "Upload file for forensic verification:",
        "btn": "🚀 Run VeriSafe AI Check",
        "orig": "Original Score",
        "fake": "Fake Score",
        "location": "Exact Modified Location",
        "verdict": "Verdict",
        "acc": "Model Accuracy Standard"
    },
    "Tamil (தமிழ்)": {
        "title": "🛡️ VeriSafe AI",
        "subtitle": "போலி புகைப்படம், வீடியோ, ஆடியோ மற்றும் ஆவணக் கண்டறிதல் தளம் (94.4% துல்லியம்)",
        "tabs": ["📷 புகைப்படம்", "🎥 வீடியோ", "🎙️ ஆடியோ", "📄 ஆவணங்கள்"],
        "upload": "ஆய்வு செய்ய கோப்பை பதிவேற்றவும்:",
        "btn": "🚀 ஆய்வு செய்",
        "orig": "உண்மை சதவீதம்",
        "fake": "போலி சதவீதம்",
        "location": "மாற்றப்பட்ட துல்லியமான இடம்",
        "verdict": "இறுதி முடிவு",
        "acc": "துல்லிய நிலவரம்"
    },
    "Hindi (हिंदी)": {
        "title": "🛡️ VeriSafe AI",
        "subtitle": "मल्टी-मॉडल दीपफेक और दस्तावेज़ धोखाधड़ी पहचान मंच (94.4% सटीकता)",
        "tabs": ["📷 फोटो विश्लेषण", "🎥 वीडियो विश्लेषण", "🎙️ ऑडियो विश्लेषण", "📄 दस्तावेज़ सत्यापन"],
        "upload": "सत्यापन के लिए फ़ाइल अपलोड करें:",
        "btn": "🚀 जांच शुरू करें",
        "orig": "मूल प्रतिशत",
        "fake": "नक्ली प्रतिशत",
        "location": "सटीक संशोधित स्थान",
        "verdict": "अंतिम परिणाम",
        "acc": "मॉडल सटीकता"
    },
    "Telugu (తెలుగు)": {
        "title": "🛡️ VeriSafe AI",
        "subtitle": "మల్టీ-మోడల్ డీప్‌ఫేక్ & డాక్యుమెంట్ ఫ్రాడ్ డిటెక్షన్ ప్లాట్‌ఫారమ్ (94.4% ఖచ్చితత్వం)",
        "tabs": ["📷 ఫోటో విశ్లేషణ", "🎥 వీడియో విశ్లేషణ", "🎙️ ఆడియో విశ్లేషణ", "📄 డాక్యుమెంట్ పరిశీలన"],
        "upload": "పరిశీలన కోసం ఫైల్‌ను అప్‌లోడ్ చేయండి:",
        "btn": "🚀 తనిఖీ చేయండి",
        "orig": "ఒరిజినల్ శాతం",
        "fake": "ఫేక్ శాతం",
        "location": "ఖచ్చితమైన మార్చబడిన ప్రదేశం",
        "verdict": "తుది నిర్ణయం",
        "acc": "ఖచ్చితత్వ ప్రమాణం"
    },
    "Malayalam (മലയാളം)": {
        "title": "🛡️ VeriSafe AI",
        "subtitle": "മൾട്ടി-മോഡൽ ഡീപ്ഫേക്ക് & ഡോക്യുമെന്റ് വ്യാജ നിർണ്ണയ പ്ലാറ്റ്ഫോം (94.4% കൃത്യത)",
        "tabs": ["📷 ഫോട്ടോ പരിശോധന", "🎥 വീഡിയോ പരിശോധന", "🎙️ ഓഡിയോ പരിശോധന", "📄 രേഖ പരിശോധന"],
        "upload": "പരിശോധിക്കാൻ ഫയൽ അപ്‌ലോഡ് ചെയ്യുക:",
        "btn": "🚀 പരിശോധിക്കുക",
        "orig": "യഥാർത്ഥ ശതമാനം",
        "fake": "വ്യാജ ശതമാനം",
        "location": "മാറ്റം വരുത്തിയ കൃത്യമായ സ്ഥലം",
        "verdict": "അന്തിമ ഫലം",
        "acc": "കൃത്യതാ മാനദണ്ഡം"
    },
    "Kannada (ಕನ್ನಡ)": {
        "title": "🛡️ VeriSafe AI",
        "subtitle": "ಬಹು-ಮಾದರಿ ಡಿಪ್‌ಫೇಕ್ ಮತ್ತು ದಾಖಲೆ ವಂಚನೆ ಪತ್ತೆ ವೇದಿಕೆ (94.4% ನಿಖರತೆ)",
        "tabs": ["📷 ಫೋಟೋ ವಿಶ್ಲೇಷಣೆ", "🎥 ವೀಡಿಯೊ ವಿಶ್ಲೇಷಣೆ", "🎙️ ಆಡಿಯೋ ವಿಶ್ಲೇಷಣೆ", "📄 ದಾಖಲೆ ಪರಿಶೀಲನೆ"],
        "upload": "ಪರಿಶೀಲನೆಗಾಗಿ ಫೈಲ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ:",
        "btn": "🚀 ತನಿಖೆ ನಡೆಸಿ",
        "orig": "ಮೂಲ ಶೇಕಡಾವಾರು",
        "fake": "ನಕಲಿ ಶೇಕಡಾವಾರು",
        "location": "ನಿಖರವಾದ ಮಾರ್ಪಡಿಸಿದ ಸ್ಥಳ",
        "verdict": "ಅಂತಿಮ ತೀರ್ಪು",
        "acc": "ನಿಖರತೆಯ ಮಾನದಂಡ"
    }
}

st.sidebar.header("🌐 Select Language / மொழி")
selected_lang = st.sidebar.selectbox("Language / மொழி:", list(I18N.keys()))
t = I18N[selected_lang]

st.title(t["title"])
st.caption(t["subtitle"])
st.markdown("---")

tabs = st.tabs(t["tabs"])

def render_detection_ui(endpoint: str, file_types: list, media_kind: str):
    uploaded = st.file_uploader(f"{t['upload']} ({media_kind})", type=file_types)
    if uploaded is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            if media_kind == "Photo":
                st.image(uploaded, use_container_width=True)
            elif media_kind == "Audio":
                st.audio(uploaded)
            elif media_kind == "Video":
                st.video(uploaded)
            else:
                st.success(f"📄 Document Loaded: {uploaded.name}")
        with col2:
            if st.button(f"{t['btn']} ({media_kind})", type="primary", use_container_width=True):
                with st.spinner("Analyzing forensics..."):
                    try:
                        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "application/octet-stream")}
                        res = requests.post(f"{BACKEND_URL}{endpoint}", files=files, timeout=30)
                        if res.status_code == 200:
                            data = res.json()
                            if data["is_fake"]:
                                st.error(f"🚨 **{t['verdict']}:** {data['verdict']}")
                            else:
                                st.success(f"✅ **{t['verdict']}:** {data['verdict']}")
                            
                            m1, m2, m3 = st.columns(3)
                            m1.metric(t["orig"], data["original_percentage"])
                            m2.metric(t["fake"], data["fake_percentage"])
                            m3.metric(t["acc"], data["accuracy_confidence"])
                            
                            st.warning(f"🎯 **{t['location']}:** `{data['modified_location']}`")
                            st.code(f"SHA-256 Hash: {data['forensic_hash']}")
                        else:
                            st.error(f"Server Error {res.status_code}: {res.text}")
                    except Exception as e:
                        st.error(f"Connection Failure: {e}")

with tabs[0]: render_detection_ui("/analyze/photo", ["jpg", "jpeg", "png", "webp"], "Photo")
with tabs[1]: render_detection_ui("/analyze/video", ["mp4", "avi", "mov"], "Video")
with tabs[2]: render_detection_ui("/analyze/audio", ["mp3", "wav", "ogg"], "Audio")
with tabs[3]: render_detection_ui("/analyze/document", ["pdf", "png", "jpg"], "Document")
