import streamlit as st
import time
import os
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px

import sys
import os
# Adjust path to import backend and components packages
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '../..')))

# Import the custom modules
from components import render_header, render_footer, require_login
from backend.model import SkinDiseaseModel

from backend.advisory import SkinAdvisoryEngine
from backend.doctor import DoctorRecommendationEngine
from backend.utils import make_gradcam_heatmap, overlay_gradcam
from backend.report import create_pdf_report
from backend.chatbot import MedicalChatbot

# 1. Page Configuration
st.set_page_config(
    page_title="SkinCare AI Pro | Diagnosis & Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_login()
render_header()

# Custom Premium Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #fafbfc !important;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in-up {
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Title Gradient */
    .gradient-text {
        background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Inputs, selectboxes, dateinputs, numberinputs styling */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input, 
    div[data-testid="stSelectbox"] div[role="combobox"],
    div[data-testid="stDateInput"] input {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.7rem 1rem !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01) !important;
    }
    div[data-testid="stTextInput"] input:focus, 
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stSelectbox"] div[role="combobox"]:focus,
    div[data-testid="stDateInput"] input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
    }
    
    /* Multiselect styling */
    div[data-testid="stMultiSelect"] div[role="combobox"] {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        min-height: 46px !important;
    }
    
    /* File Uploader styling */
    div[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 2px dashed #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(148, 163, 184, 0.05) !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #0ea5e9 !important;
        background: rgba(14, 165, 233, 0.02) !important;
        transform: translateY(-1px) !important;
    }
    div[data-testid="stFileUploader"] section {
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    }
    div[data-testid="stFileUploader"] button {
        background-color: #0ea5e9 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.5rem 1.2rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #0288d1 !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2) !important;
    }
    
    /* Images styling */
    div[data-testid="stImage"] img {
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        transition: transform 0.3s ease !important;
    }
    div[data-testid="stImage"] img:hover {
        transform: scale(1.02) !important;
    }
    
    /* Streamlit Primary Button Style */
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.25) !important;
        height: auto !important;
        padding: 0.75rem 1.5rem !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #0288d1 0%, #014377 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(14, 165, 233, 0.4) !important;
        color: white !important;
    }
    
    /* Form Label Styling */
    div[data-testid="stWidgetLabel"] p {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Doctor card styling */
    .doctor-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 1.2rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .doctor-card:hover {
        transform: translateY(-2px);
        border-color: #0ea5e9;
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.15);
        background: #ffffff;
    }
    .doc-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .doc-avatar {
        font-size: 1.8rem;
        background: #f0fdfa;
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #ccfbf1;
    }
    .doc-name {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #0f172a;
        font-size: 1.1rem;
        margin: 0;
    }
    .doc-rating {
        font-size: 0.9rem;
        font-weight: 600;
        color: #eab308;
        margin-top: 2px;
    }
    .doc-body p {
        margin: 0.3rem 0;
        font-size: 0.9rem;
        color: #475569;
    }
    .doc-distance {
        font-weight: 500;
        color: #0ea5e9 !important;
    }
    
    /* Chat message bubble improvements */
    div[data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 1rem !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02) !important;
        backdrop-filter: blur(8px) !important;
    }
    div[data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06) !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
    }
    
    /* Camera Input styling */
    div[data-testid="stCameraInput"] {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
        margin-bottom: 2rem !important;
        max-width: 500px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    div[data-testid="stCameraInput"] button {
        background-color: #0ea5e9 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Language Toggle
    lang_choice = st.radio("Select Language / भाषा चुनें", ["English", "हिंदी"])
    lang_code = 'hi' if lang_choice == "हिंदी" else 'en'
    
    st.markdown("---")
    st.info("🧠 Model Info: MobileNetV2 (HAM10000)\n\n📈 XAI: Grad-CAM Activated")

# Hardcoded Gemini API Key (Backend)
gemini_api_key = "AIzaSyBmu2oD7ej7NbHfxnpE4Oz7TN-hZt6Pe70"

# Initialize engines once (cached using Streamlit)
@st.cache_resource
def load_engines():
    inference_engine = SkinDiseaseModel()
    advisory_engine = SkinAdvisoryEngine()
    doctor_engine = DoctorRecommendationEngine()
    return inference_engine, advisory_engine, doctor_engine

# Initialize Chatbot based on Sidebar API Key
chatbot = MedicalChatbot(api_key=gemini_api_key)

# Translations Dictionary for UI Elements
ui_text = {
    'title': {"en": "🩺 AI-Based Skin Disease Diagnosis Pro", "hi": "🩺 एआई आधारित त्वचा रोग जांच प्रो"},
    'desc': {"en": "Upload a clear, close-up image of a skin lesion. This system provides Grad-CAM analysis, risk estimation, PDF reports, and AI chatbot assistance.", "hi": "त्वचा के घाव/दाग की साफ फोटो अपलोड करें। यह सिस्टम बीमारी की जांच, संभावित खतरा, पीडीएफ रिपोर्ट, और एआई चैटबॉट (AI Chatbot) की सुविधा देता है।"},
    'disclaimer': {"en": "Disclaimer: This tool provides preliminary analysis only. It is NOT a replacement for a professional medical diagnosis.", "hi": "चेतावनी: यह उपकरण केवल प्रारंभिक जांच के लिए है। यह पेशेवर चिकित्सा सलाह का विकल्प नहीं है।"},
    'upload': {"en": "Drag & Drop, Browse, or Paste (Ctrl+V) Image (JPG/PNG)", "hi": "फोटो खींचें (Drag), चुनें (Browse), या पेस्ट (Ctrl+V) करें"},
    'btn_analyze': {"en": "🔍 Analyze Image", "hi": "🔍 फोटो की जाँच करें"},
    'analyzing': {"en": "Analyzing image... (Generating Heatmaps)", "hi": "फोटो की जाँच हो रही है... (हीटमैप बन रहा है)"},
    'results': {"en": "Analysis Results", "hi": "जाँच के परिणाम"},
    'high_alert': {"en": "🚨 HIGH RISK DETECTED: Consult a dermatologist immediately!", "hi": "🚨 भारी जोखिम (HIGH RISK): तुरंत एक त्वचा विशेषज्ञ (Dermatologist) से मिलें!"},
    'precautions': {"en": "Recommended Precautions", "hi": "सुझाई गई सावधानियां (Precautions)"},
    'doctors': {"en": "📍 Nearby Dermatologists in {loc}", "hi": "📍 {loc} में आस-पास के त्वचा विशेषज्ञ"},
    'download': {"en": "📄 Download Medical Report (PDF)", "hi": "📄 मेडिकल रिपोर्ट डाउनलोड करें (PDF)"},
    'chat_title': {"en": "💬 AI Medical Assistant", "hi": "💬 एआई मेडिकल असिस्टेंट (Chatbot)"},
    'chat_prompt': {"en": "Ask me anything about your analysis...", "hi": "जांच के बारे में कुछ भी पूछें..."}
}

# 3. Main Title & Description
st.markdown(f"""
<div class="diagnosis-header" style="text-align: center; margin-bottom: 2.5rem; margin-top: 1.5rem;">
    <h1 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2.8rem; color: #0f172a; margin-bottom: 1rem;">
        <span style="background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {ui_text['title'][lang_code]}
        </span>
    </h1>
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; color: #475569; max-width: 800px; margin: 0 auto; line-height: 1.6; font-weight: 400;">
        {ui_text['desc'][lang_code]}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 2.5rem; display: flex; align-items: center; gap: 0.75rem;">
    <span style="font-size: 1.25rem;">⚠️</span>
    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.9rem; color: #b45309; font-weight: 500;">
        {ui_text['disclaimer'][lang_code]}
    </span>
</div>
""", unsafe_allow_html=True)

# Load engines inside a spinner container to keep the UI interactive and avoid white blank screen
with st.spinner("🧠 Loading AI Diagnostic Models (takes a few seconds on first run)..." if lang_code == "en" else "🧠 एआई मॉडल लोड हो रहा है (पहली बार में कुछ सेकंड लगते हैं)..."):
    inference_eng, advisory_eng, doctor_eng = load_engines()

# Chatbot Session State Init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_data" not in st.session_state:
    st.session_state.context_data = None

# Ensure temp directory for PDF parsing exists
os.makedirs("temp", exist_ok=True)

# 4. Patient Intake Form
st.markdown("---")
st.markdown(f"""
<div style="margin-top: 2rem; margin-bottom: 1.5rem;">
    <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.6rem; color: #0f172a; margin-bottom: 0.2rem;">
        📝 {"Patient Information" if lang_code == "en" else "मरीज की जानकारी"}
    </h3>
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem; color: #64748b; margin: 0;">
        {"Fill out your details to auto-generate the medical report printout" if lang_code == "en" else "मेडिकल रिपोर्ट बनाने के लिए अपनी जानकारी भरें"}
    </p>
</div>
""", unsafe_allow_html=True)

user_location = st.text_input(
    "🌍 Location (For Nearby Doctors)" if lang_code == "en" else "🌍 अपना स्थान दर्ज करें (आस-पास के डॉक्टर खोजने के लिए)", 
    "Mumbai"
)

with st.expander("Fill out your details to auto-generate the medical report printout" if lang_code == "en" else "मेडिकल रिपोर्ट बनाने के लिए अपनी जानकारी भरें", expanded=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    patient_name = c1.text_input("Full Name" if lang_code == "en" else "पूरा नाम")
    patient_age = c2.number_input("Age" if lang_code == "en" else "उम्र", min_value=1, max_value=120, value=25)
    patient_gender = c3.selectbox("Gender" if lang_code == "en" else "लिंग", ["Male", "Female", "Other"] if lang_code == "en" else ["पुरुष", "महिला", "अन्य"])
    
    st.markdown(f"""
    <div style="margin-top: 1.5rem; margin-bottom: 0.8rem;">
        <h4 style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 1.1rem; color: #0f172a; margin: 0;">
            {"Medical Context" if lang_code == "en" else "मेडिकल जानकारी"}
        </h4>
    </div>
    """, unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    duration = sc1.selectbox("Duration of Symptoms" if lang_code == "en" else "समस्या कब से है?", 
                             ["Few days", "1-4 weeks", "Months", "Years"] if lang_code == "en" else ["कुछ दिनों से", "1-4 हफ्ते से", "महीनों से", "सालों से"])
    
    symptoms = sc2.multiselect("Primary Symptoms" if lang_code == "en" else "मुख्य लक्षण",
                               ["Itching", "Pain", "Bleeding", "Scaling/Flaking", "Color Change", "Swelling"] if lang_code == "en" else ["खुजली", "दर्द", "खून आना", "पपड़ी बनना", "रंग बदलना", "सूजन"])
    
    pre_existing = st.text_input("Pre-existing Conditions (e.g. Diabetes, Hypertension, Prior Skin Cancer)" if lang_code == "en" else "पहले से कोई बीमारी (जैसे डायबिटीज, ब्लड प्रेशर, स्किन कैंसर)")
    
    report_date = st.date_input("Report Date" if lang_code == "en" else "रिपोर्ट की तारीख")

p_data = {
    "name": patient_name,
    "age": str(patient_age),
    "gender": patient_gender,
    "duration": duration,
    "symptoms": ", ".join(symptoms) if symptoms else "None reported",
    "pre_existing": pre_existing if pre_existing else "None",
    "date": str(report_date)
}


# 5. Upload Section
st.markdown(f"""
<div style="margin-top: 3rem; margin-bottom: 1.5rem;">
    <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.6rem; color: #0f172a; margin-bottom: 0.2rem;">
        📷 {"Image Input Source" if lang_code == "en" else "फोटो इनपुट का माध्यम"}
    </h3>
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem; color: #64748b; margin: 0;">
        {"Choose whether to upload an existing image file or take a live photo using your camera." if lang_code == "en" else "चुनें कि आप पहले से मौजूद फोटो अपलोड करना चाहते हैं या सीधे कैमरा से नई फोटो लेना चाहते हैं।"}
    </p>
</div>
""", unsafe_allow_html=True)

input_method = st.radio(
    "Choose Input Method / इनपुट का माध्यम चुनें",
    ["Upload File / फ़ाइल अपलोड करें", "Take Live Photo / लाइव कैमरा"],
    horizontal=True,
    label_visibility="collapsed"
)

if "Upload File" in input_method:
    uploaded_file = st.file_uploader(ui_text['upload'][lang_code], type=['jpg', 'jpeg', 'png'])
    st.markdown(f"""
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; margin-bottom: 2rem;">
        💡 <strong>{"Tip:" if lang_code == "en" else "सुझाव:"}</strong> {"You can directly drag & drop an image here, or copy an image from anywhere and press **Ctrl+V** to paste it!" if lang_code == "en" else "आप सीधे फोटो को यहाँ खींच कर डाल सकते हैं, या कहीं से भी फोटो कॉपी करके **Ctrl+V** दबाकर पेस्ट कर सकते हैं!"}
    </p>
    """, unsafe_allow_html=True)
else:
    uploaded_file = st.camera_input("Capture skin lesion / त्वचा की फोटो खींचें")

if uploaded_file is not None:
    # Three column layout: Image, GradCAM
        col_space1, col1, col2, col_space2 = st.columns([1, 3, 3, 1])

        with col1:
            st.markdown("**Original Image**" if lang_code == "en" else "**अपलोड की गई फोटो**")
            try:
                image = Image.open(uploaded_file)
                st.image(image, width=300)
                analyze_button = st.button(ui_text['btn_analyze'][lang_code], type="primary", use_container_width=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
                analyze_button = False
                
        if analyze_button:
            with st.spinner(ui_text['analyzing'][lang_code]):
                # Mock delay for UX
                time.sleep(1) 
                
                # --- A. Inference ---
                try:
                    results, preprocessed_array = inference_eng.predict(image, top_k=3)
                    top_pred_class = results[0]['class']
                    top_confidence = results[0]['confidence']
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
                    results = [{"class": "Unknown", "confidence": 0.0}]
                    preprocessed_array = None
                    top_pred_class, top_confidence = "Unknown", 0.0
                
                # --- B. Grad-CAM XAI ---
                if preprocessed_array is not None and inference_eng.is_loaded:
                    heatmap = make_gradcam_heatmap(preprocessed_array, inference_eng.model)
                    superimposed_img = overlay_gradcam(image, heatmap)
                else:
                    superimposed_img = np.array(image.convert('RGB')) # mock fallback
                
                with col2:
                    st.markdown("**XAI Heatmap (Grad-CAM)**" if lang_code == "en" else "**एआई हीटमैप (प्रभावित क्षेत्र)**")
                    st.image(superimposed_img, width=300)
            
            # Save Temp Images for PDF
            img_path, heat_path = "temp/upl.jpg", "temp/heat.jpg"
            image.convert("RGB").save(img_path)
            Image.fromarray(superimposed_img).save(heat_path)
            
            # --- C. Advisory Data ---
            info = advisory_eng.analyze(top_pred_class, top_confidence, lang=lang_code)
            st.session_state.context_data = info # Save context for chatbot
            
            st.markdown("---")
            st.markdown(f"""
            <div style="margin-top: 3rem; margin-bottom: 2rem;">
                <h2 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 2rem; color: #0f172a; margin-bottom: 0.2rem;">
                    🎯 {ui_text['results'][lang_code]}
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Smart Alert System
            if info['severity'] in ['High']:
                st.error(ui_text['high_alert'][lang_code], icon="🚨")
            
            # Premium Metrics Card
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-radius: 20px; padding: 2.2rem; border: 1px solid rgba(226,232,240,0.8); margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);">
                <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.5rem; color: #0f172a; margin-bottom: 1.5rem; margin-top: 0;">
                    🩺 {"Predicted Condition:" if lang_code == "en" else "संभावित बीमारी:"} <span style="background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">{info['name']}</span>
                </h3>
                <div style="display: flex; gap: 3rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
                    <div>
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 0.3rem;">{"Confidence Score" if lang_code == "en" else "आत्मविश्वास का स्तर"}</span>
                        <span style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: #0ea5e9;">{top_confidence:.1f}%</span>
                    </div>
                    <div>
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 0.3rem;">{"Severity Level" if lang_code == "en" else "गंभीरता का स्तर"}</span>
                        <span style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: {'#ef4444' if info['severity'] == 'High' else '#10b981'};">{info['severity']}</span>
                    </div>
                    <div>
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 0.3rem;">{"Risk Category" if lang_code == "en" else "जोखिम श्रेणी"}</span>
                        <span style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: #475569;">{info['risk_level']}</span>
                    </div>
                </div>
                <div style="background-color: #f8fafc; border-radius: 12px; padding: 1.2rem; border: 1px solid #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem; color: #334155; line-height: 1.6;">
                    <strong>{"Clinical Description:" if lang_code == "en" else "चिकित्सीय विवरण:"}</strong> {info['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- D. Confidence Visualization (Plotly) ---
            df_preds = pd.DataFrame(results)
            df_preds.rename(columns={"class": "Disease", "confidence": "Confidence (%)"}, inplace=True)
            
            # Brand Teal/Blue gradient colorscale
            custom_colorscale = [(0.0, '#38bdf8'), (0.5, '#0ea5e9'), (1.0, '#01579b')]
            
            fig = px.bar(df_preds, x="Confidence (%)", y="Disease", orientation='h', 
                         title="Top 3 Predictions Confidence" if lang_code == "en" else "संभावित बीमारियों का ग्राफ",
                         color="Confidence (%)", color_continuous_scale=custom_colorscale)
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_family='Outfit, sans-serif',
                title_font_color='#0f172a',
                title_font_size=16,
                font_family='Plus Jakarta Sans, sans-serif',
                font_color='#475569',
                xaxis=dict(showgrid=True, gridcolor='#e2e8f0', linecolor='#cbd5e1'),
                yaxis=dict(categoryorder='total ascending', showgrid=False, linecolor='#cbd5e1'),
                margin=dict(l=20, r=20, t=50, b=20),
                coloraxis_showscale=False
            )
            fig.update_traces(
                marker_line_color='rgba(0,0,0,0)',
                marker_line_width=0,
                opacity=0.9
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Precautions Card
            precautions_html = "".join([f"<li style='margin-bottom: 0.8rem;'>{prec}</li>" for prec in info['precautions']])
            st.markdown(f"""
            <div style="background: rgba(254, 242, 242, 0.6); border-radius: 20px; padding: 2.2rem; border: 1px solid rgba(254, 202, 202, 0.4); margin-bottom: 3rem; font-family: 'Plus Jakarta Sans', sans-serif;">
                <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.3rem; color: #991b1b; margin-top: 0; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem;">
                    🛑 {ui_text['precautions'][lang_code]}
                </h3>
                <ul style="color: #7f1d1d; font-size: 0.95rem; line-height: 1.6; margin: 0; padding-left: 1.2rem;">
                    {precautions_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # --- E. Doctor & PDF Report ---
            doc_col, pdf_col = st.columns([2, 1])
            with doc_col:
                st.markdown(f"""
                <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.5rem; color: #0f172a; margin-top: 0; margin-bottom: 1.5rem;">
                    {ui_text['doctors'][lang_code].format(loc=user_location)}
                </h3>
                """, unsafe_allow_html=True)
                
                doctors = doctor_eng.search_nearby_doctors(user_location)
                if doctors:
                    for doc in doctors:
                        st.markdown(f"""
                        <div class="doctor-card animate-fade-in-up">
                            <div class="doc-header">
                                <span class="doc-avatar">👩‍⚕️</span>
                                <div class="doc-details">
                                    <h4 class="doc-name">{doc['name']}</h4>
                                    <div class="doc-rating">⭐ {doc['rating']} / 5.0</div>
                                </div>
                            </div>
                            <div class="doc-body">
                                <p>📍 {doc['address']}</p>
                                <p class="doc-distance">🗺️ {doc['distance_km']} km away</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No specialists found nearby.")
            
            with pdf_col:
                st.markdown(f"""
                <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.5rem; color: #0f172a; margin-top: 0; margin-bottom: 1.5rem;">
                    {"Report" if lang_code == "en" else "रिपोर्ट"}
                </h3>
                """, unsafe_allow_html=True)
                try:
                    pdf_path = create_pdf_report(
                        img_path, heat_path, results, info, doctors, user_location, p_data
                    )
                    with open(pdf_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()

                    st.download_button(
                        label=ui_text['download'][lang_code],
                        data=PDFbyte,
                        file_name="Medical_Report.pdf",
                        mime='application/octet-stream',
                        type="primary",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")

# --- F. Chatbot System ---
if st.session_state.context_data is not None:
    st.markdown("---")
    st.markdown(f"""
    <div style="margin-top: 2rem; margin-bottom: 1.5rem;">
        <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.6rem; color: #0f172a; margin-bottom: 0.2rem;">
            {ui_text['chat_title'][lang_code]}
        </h3>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem; color: #64748b; margin: 0;">
            {"Ask follow-up questions about your diagnosis and get immediate explanations." if lang_code == "en" else "अपनी जांच के बारे में प्रश्न पूछें और तुरंत जानकारी प्राप्त करें।"}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not chatbot.is_ready():
        st.warning("⚠️ Enter your Gemini API Key in the sidebar to chat with the Medical Assistant.")
    else:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input(ui_text['chat_prompt'][lang_code]):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..." if lang_code == "en" else "सोच रहा है..."):
                    response = chatbot.generate_response(prompt, st.session_state.context_data)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

render_footer()
