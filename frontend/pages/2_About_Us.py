import streamlit as st
import sys
import os

# Adjust path to import backend and components packages
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '../..')))

from components import render_header, render_footer, get_base64_of_bin_file, require_login

st.set_page_config(
    page_title="About Us | SkinCare AI Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_login()
render_header()

assets_dir = os.path.abspath(os.path.join(current_dir, "..", "assets"))
hero_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "about_clinic.png"))
treatments_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "treatments_ai.png"))
results_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "results_face.png"))

# Use st.html to render pure HTML styles and cards, bypassing CommonMark parser quirks entirely
st.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

body {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #fafbfc !important;
}}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.animate-fade-in-up {{
    animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

/* Hero Banner */
.about-hero {{
    height: 44vh;
    min-height: 340px;
    background-image: url('data:image/png;base64,{hero_b64}');
    background-size: cover;
    background-position: center;
    border-radius: 0 0 36px 36px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.06);
}}

.hero-overlay-gradient {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.88) 0%, rgba(1, 87, 155, 0.94) 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2.5rem;
    color: white;
}}

.hero-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 0.8rem 0;
    text-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.hero-subtitle {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 300;
    max-width: 650px;
    margin: 0;
    opacity: 0.95;
    line-height: 1.6;
}}

/* Content Layout */
.about-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2.2rem;
    max-width: 1200px;
    margin: -40px auto 4rem auto;
    padding: 0 1.5rem;
    position: relative;
    z-index: 10;
}}

.about-card {{
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 22px;
    padding: 2.5rem 2rem;
    box-shadow: 0 15px 35px rgba(15, 23, 42, 0.05);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center;
}}

.about-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 25px 50px rgba(14, 165, 233, 0.12);
    border-color: rgba(14, 165, 233, 0.4);
}}

.about-icon {{
    font-size: 2.4rem;
    margin-bottom: 1.2rem;
    display: inline-block;
    background: #f0fdfa;
    padding: 0.8rem;
    border-radius: 18px;
    border: 1px solid #ccfbf1;
}}

.card-title {{
    font-family: 'Outfit', sans-serif;
    color: #0f172a;
    font-weight: 700;
    font-size: 1.4rem;
    margin-top: 0;
    margin-bottom: 0.9rem;
}}

.card-text {{
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.7;
    margin: 0;
    font-weight: 400;
}}

/* Pipeline section */
.tech-pipeline {{
    max-width: 1200px;
    margin: 1.5rem auto 5rem auto;
    padding: 0 1.5rem;
}}

.pipeline-header {{
    text-align: center;
    margin-bottom: 2.5rem;
}}

.pipeline-header h2 {{
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
}}

.pipeline-header p {{
    color: #64748b;
    font-size: 1.05rem;
    max-width: 650px;
    margin: 0 auto;
}}

.pipeline-steps {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
}}

.pipeline-box {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 2rem 1.6rem;
    position: relative;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    transition: all 0.3s ease;
}}

.pipeline-box:hover {{
    border-color: #0ea5e9;
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(14, 165, 233, 0.1);
}}

.step-number {{
    background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
    color: white;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 0.95rem;
    margin-bottom: 1.2rem;
}}

.pipeline-box h4 {{
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: #0f172a;
    margin: 0 0 0.5rem 0;
}}

.pipeline-box p {{
    font-size: 0.88rem;
    color: #64748b;
    line-height: 1.6;
    margin: 0;
}}
</style>

<div class="about-hero animate-fade-in-up">
    <div class="hero-overlay-gradient">
        <h1 class="hero-title">Pioneering Digital Health</h1>
        <p class="hero-subtitle">The Science, Deep Learning Architecture, and Clinical Vision behind SkinCare AI Pro</p>
    </div>
</div>

<div class="about-grid">
    <div class="about-card animate-fade-in-up">
        <div class="about-icon">🩺</div>
        <h3 class="card-title">Our Clinical Vision</h3>
        <p class="card-text">
            <strong>SkinCare AI Pro</strong> was designed to bridge the gap between specialized dermatology and accessible patient healthcare. By integrating deep learning with tele-health triage, we enable rapid, evidence-based preliminary assessments for everyday patients and clinicians.
        </p>
    </div>
    
    <div class="about-card animate-fade-in-up">
        <div class="about-icon">🧠</div>
        <h3 class="card-title">Deep Learning Engine</h3>
        <p class="card-text">
            Powered by high-resolution convolutional neural networks trained on the verified <strong>HAM10000</strong> medical dermatology repository. The model classifies multiple challenging skin conditions (melanocytic nevi, melanoma, basal cell carcinoma, actinic keratosis, psoriasis, and more) with high clinical sensitivity.
        </p>
    </div>
    
    <div class="about-card animate-fade-in-up">
        <div class="about-icon">🔬</div>
        <h3 class="card-title">Explainable AI (Grad-CAM)</h3>
        <p class="card-text">
            Trust in medical artificial intelligence requires absolute transparency. Our built-in <strong>Grad-CAM (Gradient-weighted Class Activation Mapping)</strong> visually highlights the exact spatial lesion boundaries and cellular pigments responsible for the model's prediction.
        </p>
    </div>
</div>

<div class="tech-pipeline animate-fade-in-up">
    <div class="pipeline-header">
        <h2>End-to-End Diagnostic Pipeline</h2>
        <p>How SkinCare AI processes camera feeds and clinical history into actionable diagnostic reports.</p>
    </div>
    
    <div class="pipeline-steps">
        <div class="pipeline-box">
            <div class="step-number">1</div>
            <h4>Image Ingestion & Normalization</h4>
            <p>Live webcam or uploaded dermatological photos are auto-cropped to square aspect ratio, contrast-balanced, and normalized for neural network tensors.</p>
        </div>
        
        <div class="pipeline-box">
            <div class="step-number">2</div>
            <h4>Deep Feature Extraction</h4>
            <p>Multi-layer convolutional kernels detect subtle dermatoscopic features including pigment networks, vascular patterns, and border irregularities.</p>
        </div>
        
        <div class="pipeline-box">
            <div class="step-number">3</div>
            <h4>XAI Heatmap Generation</h4>
            <p>Gradients of the predicted score flowing into the final convolutional layer are captured to superimpose an intuitive heat map over the patient's skin photo.</p>
        </div>
        
        <div class="pipeline-box">
            <div class="step-number">4</div>
            <h4>GPS Clinic Routing & PDF</h4>
            <p>High-precision Haversine algorithm locates verified local dermatologists by live coordinates (km/m) and auto-compiles a comprehensive medical PDF summary.</p>
        </div>
    </div>
</div>
""")

render_footer()
