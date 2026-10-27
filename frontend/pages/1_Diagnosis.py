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
from backend.model import SkinDiseaseModel, get_model_instance, preload_model_async

# Preload TensorFlow & deep learning model in the background immediately
preload_model_async()

from backend.advisory import SkinAdvisoryEngine
from backend.doctor import DoctorRecommendationEngine, fetch_user_live_location
from backend.utils import make_gradcam_heatmap, overlay_gradcam
from backend.report import create_pdf_report
from backend.chatbot import MedicalChatbot
from backend.vision_ai import MultimodalVisionEngine

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
    
    /* Completely hide sidebar and collapse button */
    section[data-testid="stSidebar"],
    div[data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }
    
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
    
    /* Input Labels Styling */
    div[data-testid="stTextInput"] label, 
    div[data-testid="stNumberInput"] label, 
    div[data-testid="stSelectbox"] label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stMultiSelect"] label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #334155 !important;
        margin-bottom: 0.4rem !important;
    }

    /* Container Card for Patient Profile */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 20px !important;
        padding: 2.2rem 2.5rem !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        border-color: #cbd5e1 !important;
        box-shadow: 0 16px 36px rgba(14, 165, 233, 0.06) !important;
    }
    
    /* Multiselect styling */
    div[data-testid="stMultiSelect"] div[role="combobox"] {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        min-height: 46px !important;
    }
    div[data-testid="stMultiSelect"] div[role="combobox"]:focus-within {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
    }
    span[data-baseweb="tag"] {
        background: #e0f2fe !important;
        border: 1px solid #bae6fd !important;
        border-radius: 8px !important;
        color: #0369a1 !important;
        font-weight: 600 !important;
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
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
        margin: 0 auto 2rem auto !important;
        max-width: 680px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stCameraInput"]:hover {
        border-color: #0ea5e9 !important;
        box-shadow: 0 12px 35px rgba(14, 165, 233, 0.1) !important;
    }
    div[data-testid="stCameraInput"] video {
        border-radius: 14px !important;
    }
    div[data-testid="stCameraInput"] button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.25) !important;
    }

    /* Ultra-Modern Medical AI Spinner & Loading Styling */
    div[data-testid="stSpinner"] {
        background: linear-gradient(135deg, rgba(240, 249, 255, 0.95) 0%, rgba(224, 242, 254, 0.85) 100%) !important;
        border: 1px solid rgba(14, 165, 233, 0.35) !important;
        border-radius: 16px !important;
        padding: 1.25rem 2rem !important;
        margin: 1.5rem auto !important;
        max-width: 650px !important;
        box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.15), 0 8px 10px -6px rgba(14, 165, 233, 0.1) !important;
        backdrop-filter: blur(16px) !important;
        animation: fadeInUp 0.4s ease forwards !important;
    }
    div[data-testid="stSpinner"] > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.85rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        color: #0369a1 !important;
        letter-spacing: 0.2px !important;
    }
    div[data-testid="stSpinner"] svg {
        stroke: #0ea5e9 !important;
        width: 28px !important;
        height: 28px !important;
        filter: drop-shadow(0 0 8px rgba(14, 165, 233, 0.5)) !important;
    }
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Automatically load API key from .env file
env_file = os.path.abspath(os.path.join(current_dir, "../..", ".env"))
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()

active_gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()

# 2. Engine & Language State Initialization
all_engine_modes = [
    "✨ Hybrid (CNN + Multimodal Vision AI)",
    "🧬 Local Deep Learning (Fitzpatrick 17k + HAM10000 CNN)",
    "🧠 Multimodal Vision AI Only"
]

if 'engine_mode' not in st.session_state:
    st.session_state.engine_mode = all_engine_modes[0]

if 'lang_choice' not in st.session_state:
    st.session_state.lang_choice = "English"

lang_choice = st.session_state.get('lang_choice', 'English')
lang_code = 'hi' if lang_choice == "हिंदी" else 'en'
engine_mode = st.session_state.get('engine_mode', all_engine_modes[0])

# Initialize engines with show_spinner=False so no raw Streamlit runner text is shown
@st.cache_resource(show_spinner=False)
def load_engines():
    inference_engine = get_model_instance()
    advisory_engine = SkinAdvisoryEngine()
    doctor_engine = DoctorRecommendationEngine()
    return inference_engine, advisory_engine, doctor_engine

# Initialize Chatbot with user's active key if provided
chatbot = MedicalChatbot(api_key=active_gemini_key)

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
<div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
    <span style="font-size: 1.25rem;">⚠️</span>
    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.9rem; color: #b45309; font-weight: 500;">
        {ui_text['disclaimer'][lang_code]}
    </span>
</div>
""", unsafe_allow_html=True)

# 3.1 AI Diagnostic Engine & Language Configuration Bar (Front and Center on Main Screen)
with st.container(border=True):
    cfg_col1, cfg_col2, cfg_col3 = st.columns([3.2, 1.8, 2.0], gap="medium")
    
    with cfg_col1:
        cur_eng = st.session_state.get('engine_mode', all_engine_modes[0])
        cur_idx = all_engine_modes.index(cur_eng) if cur_eng in all_engine_modes else 0
        engine_mode = st.selectbox(
            "🧠 Diagnostic Model / डायग्नोसिस मॉडल चुनें",
            all_engine_modes,
            index=cur_idx,
            key="main_ai_engine",
            help="Hybrid combines CNN Grad-CAM with Multimodal Vision AI for acne, pimples, and complex skin lesions."
        )
        st.session_state.engine_mode = engine_mode

    with cfg_col2:
        new_lang = st.radio(
            "🌐 Select Language / भाषा चुनें",
            ["English", "हिंदी"],
            index=0 if lang_choice == "English" else 1,
            horizontal=True,
            key="main_lang_choice"
        )
        if new_lang != st.session_state.lang_choice:
            st.session_state.lang_choice = new_lang
            st.rerun()

    with cfg_col3:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 0.65rem 0.9rem; margin-top: 1.45rem;">
            <div style="font-weight: 700; color: #047857; font-size: 0.86rem; display: flex; align-items: center; gap: 0.4rem;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                {"AI Engine Connected" if lang_code == "en" else "एआई इंजन कनेक्टेड"}
            </div>
            <div style="font-size: 0.75rem; color: #475569; margin-top: 0.2rem; line-height: 1.35;">
                <strong>Gemini 2.5 Flash</strong> + <strong>MobileNetV2</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chatbot Session State Init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_data" not in st.session_state:
    st.session_state.context_data = None
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "last_image_hash" not in st.session_state:
    st.session_state.last_image_hash = None
if "user_location_text" not in st.session_state:
    # Auto-detect live location silently on first visit
    detected_loc = fetch_user_live_location()
    st.session_state.user_location_text = detected_loc.get("formatted", "Pune, Maharashtra")
    st.session_state.user_coords = (detected_loc.get("lat", 18.62698), detected_loc.get("lon", 73.78301))
if "user_coords" not in st.session_state:
    st.session_state.user_coords = (18.62698, 73.78301)

# Ensure temp directory for PDF parsing exists
os.makedirs("temp", exist_ok=True)

# 4. Patient Intake Form
st.markdown("---")
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 2.2rem; margin-bottom: 1.2rem; flex-wrap: wrap; gap: 1rem;">
    <div>
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
            <span style="font-size: 1.5rem;">📋</span>
            <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.65rem; color: #0f172a; margin: 0;">
                {"Patient Clinical Profile" if lang_code == "en" else "मरीज का क्लिनिकल प्रोफाइल"}
            </h3>
        </div>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.95rem; color: #64748b; margin: 0;">
            {"Enter demographic and symptom history to customize AI diagnostic precision and PDF report." if lang_code == "en" else "सटीक जांच और मेडिकल पीडीएफ रिपोर्ट बनाने के लिए मरीज की जानकारी भरें।"}
        </p>
    </div>
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.08) 0%, rgba(2, 132, 199, 0.04) 100%); border: 1px solid rgba(14, 165, 233, 0.25); padding: 0.45rem 1rem; border-radius: 999px; display: inline-flex; align-items: center; gap: 0.45rem;">
        <span style="font-size: 0.85rem;">📄</span>
        <span style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 700; color: #0284c7; text-transform: uppercase; letter-spacing: 0.5px;">
            {"Auto-generates PDF Report" if lang_code == "en" else "पीडीएफ रिपोर्ट तैयार होगी"}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    # Part 1: Personal & Demographic Details
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 1px solid #f1f5f9;">
        <span style="font-size: 1.15rem;">👤</span>
        <span style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; color: #0f172a;">
            {"Personal & Demographic Details" if lang_code == "en" else "व्यक्तिगत जानकारी"}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    r1_c1, r1_c2, r1_c3, r1_c4 = st.columns([2.5, 1.1, 1.5, 2.9])
    patient_name = r1_c1.text_input(
        "Full Name" if lang_code == "en" else "पूरा नाम",
        placeholder="e.g. John Doe / राहुल शर्मा"
    )
    patient_age = r1_c2.number_input(
        "Age" if lang_code == "en" else "उम्र",
        min_value=1,
        max_value=120,
        value=25
    )
    patient_gender = r1_c3.selectbox(
        "Gender" if lang_code == "en" else "लिंग",
        ["Male", "Female", "Other"] if lang_code == "en" else ["पुरुष", "महिला", "अन्य"]
    )
    
    with r1_c4:
        loc_input_col, loc_btn_col = st.columns([2.2, 1.1])
        with loc_input_col:
            user_location = st.text_input(
                "City / Location" if lang_code == "en" else "शहर / स्थान",
                value=st.session_state.get('user_location_text', 'Pune, Maharashtra'),
                help="Used to match top-rated dermatologists and skin clinics near your live coordinates."
            )
            st.session_state.user_location_text = user_location
        with loc_btn_col:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("📍 Live", help="Fetch your live GPS / IP location", use_container_width=True):
                with st.spinner("Detecting location..."):
                    live_res = fetch_user_live_location()
                    st.session_state.user_location_text = live_res["formatted"]
                    st.session_state.user_coords = (live_res["lat"], live_res["lon"])
                    st.toast(f"📍 Live Location Detected: {live_res['formatted']}", icon="📍")
                    st.rerun()
        if st.session_state.get('user_coords'):
            st.markdown(f"""
            <div style="font-size: 0.76rem; color: #0284c7; display: flex; align-items: center; gap: 0.3rem; margin-top: -8px;">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10b981;"></span>
                {"Live GPS Active" if lang_code == "en" else "लाइव जीपीएस सक्रिय"} ({st.session_state.user_coords[0]:.2f}°, {st.session_state.user_coords[1]:.2f}°)
            </div>
            """, unsafe_allow_html=True)
    
    # Part 2: Clinical Context & Medical History
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 1.6rem; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 1px solid #f1f5f9;">
        <span style="font-size: 1.15rem;">🩺</span>
        <span style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; color: #0f172a;">
            {"Clinical Context & Symptom History" if lang_code == "en" else "क्लिनिकल स्थिति और लक्षण इतिहास"}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    r2_c1, r2_c2 = st.columns([1, 1.6])
    duration = r2_c1.selectbox(
        "Duration of Symptoms" if lang_code == "en" else "समस्या कब से है?",
        ["Few days", "1-4 weeks", "Months", "Years"] if lang_code == "en" else ["कुछ दिनों से", "1-4 हफ्ते से", "महीनों से", "सालों से"]
    )
    symptoms = r2_c2.multiselect(
        "Primary Symptoms" if lang_code == "en" else "मुख्य लक्षण",
        ["Itching", "Pain", "Bleeding", "Scaling/Flaking", "Color Change", "Swelling"] if lang_code == "en" else ["खुजली", "दर्द", "खून आना", "पपड़ी बनना", "रंग बदलना", "सूजन"],
        placeholder="Select any noticed symptoms..." if lang_code == "en" else "लक्षण चुनें..."
    )
    
    r3_c1, r3_c2 = st.columns([2.5, 1])
    pre_existing = r3_c1.text_input(
        "Pre-existing Conditions / Medical Notes" if lang_code == "en" else "पहले से कोई बीमारी या एलर्जी",
        placeholder="e.g. Diabetes, Hypertension, Prior Eczema, None / कोई नहीं"
    )
    report_date = r3_c2.date_input(
        "Assessment Date" if lang_code == "en" else "जांच की तारीख"
    )

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
    key="diag_input_method"
)

uploaded_file = None
if "Upload File" in input_method:
    uploaded_file = st.file_uploader(
        ui_text['upload'][lang_code], 
        type=['jpg', 'jpeg', 'png'],
        key="diag_file_uploader"
    )
    st.markdown(f"""
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; margin-bottom: 2rem;">
        💡 <strong>{"Tip:" if lang_code == "en" else "सुझाव:"}</strong> {"You can directly drag & drop an image here, or copy an image from anywhere and press **Ctrl+V** to paste it!" if lang_code == "en" else "आप सीधे फोटो को यहाँ खींच कर डाल सकते हैं, या कहीं से भी फोटो कॉपी करके **Ctrl+V** दबाकर पेस्ट कर सकते हैं!"}
    </p>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.08) 0%, rgba(2, 132, 199, 0.03) 100%); border: 1.5px dashed rgba(14, 165, 233, 0.35); border-radius: 18px; padding: 1.2rem 1.6rem; margin-bottom: 1.2rem; text-align: center;">
        <div style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.1rem; color: #0369a1; display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 0.35rem;">
            <span>🎯</span> {"Clinical Camera Scanner Guidance" if lang_code == "en" else "कैमरा स्कैनर निर्देश"}
        </div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.88rem; color: #475569; line-height: 1.5;">
            {"For accurate disease detection, hold your camera **4–6 inches (10–15 cm)** close to the lesion with good lighting, centering the affected skin area in the frame." if lang_code == "en" else "सटीक जांच के लिए कैमरे को त्वचा के दाग/घाव के **10–15 सेमी (4–6 इंच)** पास रखें, अच्छी रोशनी सुनिश्चित करें और प्रभावित हिस्से को फ्रेम के बीच में रखें।"}
        </div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.camera_input("Capture skin lesion / त्वचा की फोटो खींचें", key="diag_camera_scanner")

if uploaded_file is not None:
    # Track file identity so uploading a new photo resets previous analysis
    import hashlib
    import io
    img_bytes = uploaded_file.getvalue()
    current_hash = hashlib.md5(img_bytes).hexdigest()
    if st.session_state.get('last_image_hash') != current_hash:
        st.session_state.last_image_hash = current_hash
        st.session_state.analysis_data = None
        st.session_state.context_data = None

    try:
        image = Image.open(io.BytesIO(img_bytes))
    except Exception as e:
        st.error(f"Error loading image: {e}")
        image = None

    if image is not None:
        # Two-column layout for Image & XAI Heatmap
        img_col1, img_col2 = st.columns(2, gap="large")

        with img_col1:
            st.markdown(f"#### 📷 {'Original Lesion Image' if lang_code == 'en' else 'स्कैन की गई त्वचा की फोटो'}")
            st.image(image, use_container_width=True)
            analyze_button = st.button(ui_text['btn_analyze'][lang_code], type="primary", use_container_width=True, key="btn_run_analysis")

        if analyze_button:
            with st.spinner(ui_text['analyzing'][lang_code]):
                inference_eng, advisory_eng, doctor_eng = load_engines()
                
                # --- A. Local CNN Inference & Grad-CAM ---
                try:
                    cnn_results, preprocessed_array = inference_eng.predict(image, top_k=3)
                    cnn_top_pred = cnn_results[0]['class']
                    cnn_confidence = cnn_results[0]['confidence']
                except Exception as e:
                    cnn_results = [{"class": "Unknown", "confidence": 0.0}]
                    preprocessed_array = None
                    cnn_top_pred, cnn_confidence = "Unknown", 0.0
                
                # Generate Grad-CAM XAI Heatmap
                if preprocessed_array is not None and inference_eng.is_loaded:
                    heatmap = make_gradcam_heatmap(preprocessed_array, inference_eng.model)
                    superimposed_img = overlay_gradcam(image, heatmap)
                else:
                    superimposed_img = np.array(image.convert('RGB'))
                
                # --- B. Multimodal Vision AI Execution (if active) ---
                vision_used = False
                active_key = st.session_state.get('user_gemini_key', os.environ.get('GEMINI_API_KEY', '')).strip()
                vision_eng = MultimodalVisionEngine(api_key=active_key)

                if "Local Deep Learning" not in engine_mode and vision_eng.is_available():
                    with st.spinner("Analyzing with Multimodal Vision AI..."):
                        vision_data, vision_err = vision_eng.analyze_lesion(image, p_data, lang=lang_code)
                        if vision_data:
                            results = vision_data['results']
                            info = vision_data['info']
                            top_pred_class = vision_data['top_pred_class']
                            top_confidence = vision_data['top_confidence']
                            engine_label = "🧠 Multimodal Vision AI (Gemini 2.5 Flash)"
                            vision_used = True
                        else:
                            st.toast(f"Vision AI notice: {vision_err}. Using Local CNN model.", icon="ℹ️")

                if not vision_used:
                    results = cnn_results
                    top_pred_class = cnn_top_pred
                    top_confidence = cnn_confidence
                    info = advisory_eng.analyze(top_pred_class, top_confidence, lang=lang_code)
                    engine_label = "🧬 Local Deep Learning (MobileNetV2 CNN)"
                
                # Save Temp Images for PDF
                img_path, heat_path = "temp/upl.jpg", "temp/heat.jpg"
                image.convert("RGB").save(img_path)
                Image.fromarray(superimposed_img).save(heat_path)
                
                st.session_state.context_data = info # Save context for chatbot
                
                # --- C. Doctor Recommendations ---
                u_lat, u_lon = st.session_state.get('user_coords', (None, None))
                doctors = doctor_eng.search_nearby_doctors(user_location, user_lat=u_lat, user_lon=u_lon)
                
                # --- D. Pre-Generate PDF Report ---
                try:
                    pdf_path = create_pdf_report(
                        img_path, heat_path, results, info, doctors, user_location, p_data
                    )
                    with open(pdf_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()
                except Exception as e:
                    PDFbyte = None
                
                # Store persistently in session state so clicking download never clears the results!
                st.session_state.analysis_data = {
                    'results': results,
                    'top_pred_class': top_pred_class,
                    'top_confidence': top_confidence,
                    'superimposed_img': superimposed_img,
                    'info': info,
                    'doctors': doctors,
                    'pdf_bytes': PDFbyte,
                    'img_path': img_path,
                    'heat_path': heat_path,
                    'engine_label': engine_label
                }
                st.rerun()

        # Display Grad-CAM in the second column if analysis exists
        with img_col2:
            if st.session_state.get('analysis_data') is not None:
                st.markdown(f"#### 🔬 {'XAI Heatmap (Affected Region)' if lang_code == 'en' else 'एआई हीटमैप (प्रभावित क्षेत्र)'}")
                st.image(st.session_state.analysis_data['superimposed_img'], use_container_width=True)
            else:
                st.markdown(f"#### 🔬 {'XAI Heatmap' if lang_code == 'en' else 'एआई हीटमैप'}")
                st.markdown(f"""
                <div style="background: rgba(248, 250, 252, 0.8); border: 2px dashed #cbd5e1; border-radius: 16px; min-height: 250px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2rem;">
                    <span style="font-size: 2.4rem; margin-bottom: 0.6rem;">🔬</span>
                    <h4 style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; color: #475569; margin: 0;">{"AI Heatmap Standby" if lang_code == "en" else "एआई हीटमैप स्टैंडबाय"}</h4>
                    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #94a3b8; margin: 0.5rem 0 0 0;">{"Click 'Analyze Image' to scan and highlight cellular pigment patterns" if lang_code == "en" else "जांच शुरू करने के लिए Analyze Image पर क्लिक करें"}</p>
                </div>
                """, unsafe_allow_html=True)

        # Persistent Results Section (survives PDF download and page reruns!)
        if st.session_state.get('analysis_data') is not None:
            ad = st.session_state.analysis_data
            results = ad['results']
            top_pred_class = ad['top_pred_class']
            top_confidence = ad['top_confidence']
            info = ad['info']
            doctors = ad['doctors']
            PDFbyte = ad['pdf_bytes']
            img_path = ad['img_path']
            heat_path = ad['heat_path']
            engine_label = ad.get('engine_label', '🧬 Local Deep Learning (MobileNetV2 CNN)')

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
                <div style="display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.25); color: #0284c7; padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.82rem; font-weight: 700; margin-bottom: 1.2rem; font-family: 'Outfit', sans-serif;">
                    {engine_label}
                </div>
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
                
                if doctors:
                    for doc in doctors:
                        st.markdown(f"""
                        <div class="doctor-card animate-fade-in-up" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.3rem 1.5rem; margin-bottom: 1.1rem; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03); transition: all 0.3s ease;">
                            <div class="doc-header" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                                <div style="display: flex; gap: 0.9rem; align-items: center;">
                                    <span class="doc-avatar" style="font-size: 1.6rem; background: #e0f2fe; padding: 0.5rem; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center;">🏥</span>
                                    <div>
                                        <h4 class="doc-name" style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700; color: #0f172a;">{doc['name']}</h4>
                                        <div class="doc-rating" style="color: #eab308; font-size: 0.88rem; font-weight: 600; margin-top: 2px;">⭐ {doc['rating']} / 5.0 • {"Verified Skin Specialist" if lang_code == "en" else "सत्यापित त्वचा विशेषज्ञ"}</div>
                                    </div>
                                </div>
                                <span style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); color: white; padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.85rem; font-weight: 700; font-family: 'Outfit', sans-serif; letter-spacing: 0.5px; box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3); white-space: nowrap;">
                                    🧭 {doc.get('distance_str', f"{doc['distance_km']} km")} away
                                </span>
                            </div>
                            <div class="doc-body" style="font-size: 0.9rem; color: #475569; margin-top: 0.5rem; line-height: 1.5;">
                                <p style="margin: 0.2rem 0; color: #334155;">📍 <strong>{"Address:" if lang_code == "en" else "पता:"}</strong> {doc['address']}</p>
                                <div style="margin-top: 0.9rem;">
                                    <a href="{doc['maps_url']}" target="_blank" style="display: inline-flex; align-items: center; gap: 0.4rem; background: #f8fafc; border: 1px solid #cbd5e1; color: #0369a1; padding: 0.45rem 1rem; border-radius: 9px; font-size: 0.84rem; font-weight: 600; text-decoration: none; transition: all 0.2s ease;">
                                        🗺️ {"Navigate on Google Maps →" if lang_code == "en" else "गूगल मैप्स पर रास्ता देखें →"}
                                    </a>
                                </div>
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
                if PDFbyte is not None:
                    st.download_button(
                        label=ui_text['download'][lang_code],
                        data=PDFbyte,
                        file_name="Medical_Report.pdf",
                        mime='application/octet-stream',
                        type="primary",
                        use_container_width=True
                    )
                else:
                    st.warning("Report generation in progress...")

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
