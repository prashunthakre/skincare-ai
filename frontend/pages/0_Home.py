import streamlit as st
import sys
import os

# Adjust path to import backend and components packages
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '../..')))

from components import render_header, render_footer, get_base64_of_bin_file, require_login

st.set_page_config(
    page_title="SkinCare AI Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_login()

# Manage welcome popup with placeholder to maintain element order across reruns
welcome_placeholder = st.empty()
if st.session_state.get('show_welcome_popup', False):
    st.session_state.show_welcome_popup = False
    user_name = st.session_state.get('user_name', 'User')
    welcome_placeholder.markdown(f"""
    <style>
    @keyframes popupAnim {{
        0% {{ opacity: 0; transform: translate(-50%, -45%) scale(0.9); }}
        8% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
        90% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
        100% {{ opacity: 0; transform: translate(-50%, -55%) scale(0.95); visibility: hidden; pointer-events: none; }}
    }}
    .welcome-popup {{
        position: fixed;
        top: 50%;
        left: 50%;
        background: rgba(15, 23, 42, 0.95);
        color: white;
        padding: 3rem 5rem;
        border-radius: 24px;
        z-index: 999999;
        text-align: center;
        box-shadow: 0 25px 60px rgba(0,0,0,0.4), 0 0 1px 1px rgba(255,255,255,0.1) inset;
        animation: popupAnim 4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        pointer-events: none;
        backdrop-filter: blur(12px);
    }}
    .welcome-popup h1 {{
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #38bdf8 0%, #2dd4bf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }}
    .welcome-popup h3 {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.5rem;
        font-weight: 300;
        color: #94a3b8;
        margin-top: 15px;
        letter-spacing: 0.5px;
    }}
    </style>
    <div class="welcome-popup">
        <h1>Hello, {user_name}!</h1>
        <h3>Welcome to SkinCare AI Pro</h3>
    </div>
    """, unsafe_allow_html=True)

# Load Images safely using relative pathing
assets_dir = os.path.abspath(os.path.join(current_dir, "..", "assets"))
hero_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "hero_bg.png"))
about_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "about_clinic.png"))
treatments_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "treatments_ai.png"))
results_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "results_face.png"))

render_header()

# CSS for the premium homepage layout with rich animations and styles
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    body {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1e293b;
        background-color: #fafbfc;
    }}

    /* Animations */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    @keyframes scaleUp {{
        from {{ opacity: 0; transform: scale(0.97); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}

    @keyframes kenBurns {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.04); }}
        100% {{ transform: scale(1); }}
    }}

    @keyframes pulseGlow {{
        0% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.4); }}
        70% {{ box-shadow: 0 0 0 12px rgba(14, 165, 233, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }}
    }}

    /* Utility Styles */
    .animate-fade-in {{ animation: fadeIn 1.2s ease forwards; }}
    .animate-fade-in-up {{ animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
    .animation-delay-1 {{ animation-delay: 0.15s; opacity: 0; }}
    .animation-delay-2 {{ animation-delay: 0.3s; opacity: 0; }}
    .animation-delay-3 {{ animation-delay: 0.45s; opacity: 0; }}

    /* Gradient Text */
    .gradient-text {{
        background: linear-gradient(135deg, #0ea5e9 0%, #0288d1 50%, #01579b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Hero Section */
    .hero-container {{
        position: relative;
        height: 85vh;
        min-height: 650px;
        overflow: hidden;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.05);
    }}

    .hero-bg-zoom {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url('data:image/png;base64,{hero_b64}');
        background-size: cover;
        background-position: center 30%;
        animation: kenBurns 20s ease-in-out infinite;
        z-index: 0;
    }}

    .hero-overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, rgba(255,255,255,0.96) 0%, rgba(255,255,255,0.8) 40%, rgba(255,255,255,0.15) 100%);
        z-index: 1;
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
        max-width: 700px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 6%;
    }}

    .hero-content h1 {{
        font-family: 'Outfit', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.15;
        color: #0f172a;
        margin-bottom: 1.5rem;
    }}

    .hero-content p {{
        font-size: 1.25rem;
        color: #475569;
        line-height: 1.75;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }}

    /* Premium Custom Button */
    .btn-premium {{
        background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
        color: white !important;
        padding: 1.1rem 2.8rem;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        display: inline-block;
        width: fit-content;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .btn-premium:hover {{
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(14, 165, 233, 0.4);
        background: linear-gradient(135deg, #0288d1 0%, #014377 100%);
    }}

    /* Global Section Title */
    .section-header {{
        text-align: center !important;
        margin-bottom: 5rem !important;
        display: block !important;
        width: 100% !important;
    }}

    .section-title {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.8rem !important;
        color: #0f172a !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
        display: block !important;
    }}

    .section-subtitle {{
        color: #64748b !important;
        font-size: 1.15rem !important;
        max-width: 600px !important;
        margin: 0 auto !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
        text-align: center !important;
        display: block !important;
    }}

    /* Why Choose Us Section */
    .why-sec {{
        background-color: #f8fafc;
        padding: 8rem 5%;
        position: relative;
    }}

    .why-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2.5rem;
        max-width: 1250px;
        margin: 0 auto;
    }}

    .why-card {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.02);
    }}

    .why-card:hover {{
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 25px 50px rgba(14, 165, 233, 0.12);
        border-color: rgba(14, 165, 233, 0.3);
    }}

    .icon-box {{
        width: 75px; height: 75px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(45, 212, 191, 0.1) 100%);
        color: #0288d1;
        display: flex; justify-content: center; align-items: center;
        font-size: 2.2rem;
        margin: 0 auto 2rem auto;
        transition: all 0.4s ease;
    }}

    .why-card:hover .icon-box {{
        transform: scale(1.1) rotate(5deg);
        background: linear-gradient(135deg, #0ea5e9 0%, #2dd4bf 100%);
        color: white;
    }}

    .why-card h4 {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.35rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #0f172a;
    }}

    .why-card p {{
        color: #64748b;
        font-size: 1rem;
        line-height: 1.7;
    }}

    /* Features Section */
    .features-sec {{
        padding: 8rem 5%;
        background-color: white;
    }}

    .features-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
        gap: 3rem;
        max-width: 1250px;
        margin: 0 auto;
    }}

    .feat-card-container {{
        background: white;
        border-radius: 28px;
        overflow: hidden;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .feat-card-container:hover {{
        transform: translateY(-8px);
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.08);
        border-color: #e2e8f0;
    }}

    .feat-img-wrapper {{
        overflow: hidden;
        height: 250px;
        position: relative;
    }}

    .feat-card-img {{
        width: 100%; height: 100%;
        object-fit: cover;
        transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .feat-card-container:hover .feat-card-img {{
        transform: scale(1.07);
    }}

    .feat-card-content {{
        padding: 2.2rem;
    }}

    .feat-card-content h4 {{
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }}

    .feat-card-content p {{
        color: #64748b;
        font-size: 0.98rem;
        line-height: 1.65;
        margin-bottom: 1.8rem;
        height: 70px;
        overflow: hidden;
    }}

    .feat-card-link {{
        text-decoration: none;
        color: #0ea5e9;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
        width: fit-content;
    }}

    .feat-card-link:hover {{
        color: #01579b;
        transform: translateX(4px);
    }}

    /* About Us Section with Stats */
    .about-sec {{
        padding: 8rem 5%;
        background-color: #f8fafc;
    }}

    .about-split {{
        display: flex;
        flex-wrap: wrap;
        gap: 4rem;
        max-width: 1250px;
        margin: 0 auto;
        align-items: center;
    }}

    .about-visual {{
        flex: 1;
        min-width: 300px;
        position: relative;
    }}

    .about-img-frame {{
        width: 100%;
        border-radius: 32px;
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.12);
        display: block;
        transition: all 0.4s ease;
    }}

    .about-visual:hover .about-img-frame {{
        transform: scale(1.02);
    }}

    .about-badge-glow {{
        position: absolute;
        bottom: -20px;
        right: -20px;
        background: white;
        padding: 1.5rem 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        border: 1px solid #f1f5f9;
        display: flex;
        flex-direction: column;
        animation: pulseGlow 3s infinite;
    }}

    .about-badge-glow span.number {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #0ea5e9;
        line-height: 1;
    }}

    .about-badge-glow span.label {{
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .about-text-content {{
        flex: 1.2;
        min-width: 320px;
    }}

    .about-text-content h2 {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 2rem;
        line-height: 1.2;
    }}

    .about-text-content p {{
        font-size: 1.15rem;
        line-height: 1.8;
        color: #475569;
        margin-bottom: 2.5rem;
    }}

    .stats-row {{
        display: flex;
        gap: 3rem;
        border-top: 1px solid #e2e8f0;
        padding-top: 2rem;
    }}

    .stat-item h3 {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 5px 0;
    }}

    .stat-item p {{
        color: #64748b;
        font-size: 0.95rem;
        margin: 0;
    }}

    /* Difference Section */
    .diff-sec {{
        padding: 8rem 5%;
        background-color: #0f172a;
        color: white;
        text-align: center;
    }}

    .diff-sec h2 {{
        color: white;
    }}

    .diff-sec p {{
        color: #94a3b8;
    }}

    .diff-visual-container {{
        max-width: 950px;
        margin: 4rem auto 0 auto;
        position: relative;
        border-radius: 28px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 40px 80px rgba(0,0,0,0.5);
    }}

    .diff-img-glow {{
        width: 100%;
        height: auto;
        max-height: 550px;
        object-fit: cover;
        display: block;
        transition: transform 0.5s ease;
    }}

    .diff-visual-container:hover .diff-img-glow {{
        transform: scale(1.01);
    }}

    .diff-active-tag {{
        position: absolute;
        top: 25px;
        left: 25px;
        background: rgba(15, 23, 42, 0.85);
        color: #38bdf8;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.3);
        display: flex;
        align-items: center;
        gap: 8px;
        backdrop-filter: blur(8px);
    }}

    .pulse-dot {{
        width: 8px; height: 8px;
        background-color: #38bdf8;
        border-radius: 50%;
        display: inline-block;
        animation: pulseGlow 1.5s infinite;
    }}
</style>

<!-- HERO SECTION -->
<div class="hero-container">
    <div class="hero-bg-zoom"></div>
    <div class="hero-overlay"></div>
    <div class="hero-content animate-fade-in-up">
        <h1>Discover Radiant Skin<br>With <span class="gradient-text">AI-Driven</span> Diagnosis</h1>
        <p>Empowering both patients and doctors with real-time, explainable diagnostic imaging to catch skin diseases early and enhance natural well-being through digital trust.</p>
        <a href="/Diagnosis" target="_self" class="btn-premium">Get Free Diagnosis</a>
    </div>
</div>

<!-- WHY CHOOSE US -->
<div class="why-sec">
    <div class="section-header animate-fade-in-up animation-delay-1">
        <h2 class="section-title">Why Choose Us?</h2>
        <p class="section-subtitle">At SkinCare AI, we believe in technology mapping to safety. Here is why we stand out.</p>
    </div>
    <div class="why-grid">
        <div class="why-card animate-fade-in-up animation-delay-1">
            <div class="icon-box">🔬</div>
            <h4>Advanced AI Models</h4>
            <p>Our deep learning models are trained on the verified HAM10000 medical dataset for top-tier analysis.</p>
        </div>
        <div class="why-card animate-fade-in-up animation-delay-2">
            <div class="icon-box">📄</div>
            <h4>Structured PDF Reports</h4>
            <p>Instantly generate professional, comprehensive assessment PDFs to bring to your dermatologist.</p>
        </div>
        <div class="why-card animate-fade-in-up animation-delay-3">
            <div class="icon-box">⚡</div>
            <h4>Instant Explanations</h4>
            <p>Receive immediate Grad-CAM visual heatmaps showcasing precisely which regions the AI focused on.</p>
        </div>
    </div>
</div>

<!-- OUR FEATURES -->
<div class="features-sec">
    <div class="section-header animate-fade-in-up">
        <h2 class="section-title">AI Diagnostics Toolkit</h2>
        <p class="section-subtitle">Tailored deep learning modules built to provide rapid screening and diagnostic confidence.</p>
    </div>
    <div class="features-grid">
        <div class="feat-card-container animate-fade-in-up animation-delay-1">
            <div class="feat-img-wrapper">
                <img class="feat-card-img" src="data:image/png;base64,{treatments_b64}">
            </div>
            <div class="feat-card-content">
                <h4>Grad-CAM Heatmaps</h4>
                <p>Explainable AI outputs highlight alarming lesions so you know exactly what is being analyzed.</p>
                <a href="/Diagnosis" target="_self" class="feat-card-link">Try Diagnostic Tool →</a>
            </div>
        </div>
        <div class="feat-card-container animate-fade-in-up animation-delay-2">
            <div class="feat-img-wrapper">
                <img class="feat-card-img" src="data:image/png;base64,{results_b64}">
            </div>
            <div class="feat-card-content">
                <h4>Smart Severity Warning</h4>
                <p>Categorizes risks into low, moderate, or high alerts dynamically based on prediction weights.</p>
                <a href="/Diagnosis" target="_self" class="feat-card-link">Check Severity Levels →</a>
            </div>
        </div>
        <div class="feat-card-container animate-fade-in-up animation-delay-3">
            <div class="feat-img-wrapper">
                <img class="feat-card-img" src="data:image/png;base64,{about_b64}">
            </div>
            <div class="feat-card-content">
                <h4>Medical Chatbot Assistant</h4>
                <p>An intelligent chatbot customized with your analysis context to address questions immediately.</p>
                <a href="/Diagnosis" target="_self" class="feat-card-link">Consult Chatbot →</a>
            </div>
        </div>
    </div>
</div>

<!-- ABOUT US WITH STATS -->
<div class="about-sec">
    <div class="about-split">
        <div class="about-visual animate-fade-in-up">
            <img class="about-img-frame" src="data:image/png;base64,{about_b64}">
            <div class="about-badge-glow">
                <span class="number">98.2%</span>
                <span class="label">AI Confidence</span>
            </div>
        </div>
        <div class="about-text-content animate-fade-in-up animation-delay-1">
            <h2>Pioneering Digital Health & Explainable Medicine</h2>
            <p>At SkinCare AI Pro, we believe that early screening is a vital component of proactive self-care. Founded by dermatologists and computer vision scientists, we bridge the gap between AI and patient care by offering clear, explainable, and accessible diagnostics.</p>
            <div class="stats-row">
                <div class="stat-item">
                    <h3>10+</h3>
                    <p>Lesion Categories</p>
                </div>
                <div class="stat-item">
                    <h3>15k+</h3>
                    <p>Dataset Images</p>
                </div>
                <div class="stat-item">
                    <h3>Zero</h3>
                    <p>Wait Time</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- DIFFERENCE IN RESULTS (GRAD-CAM SCREEN) -->
<div class="diff-sec">
    <div class="section-header animate-fade-in-up">
        <h2 class="section-title">Explainable AI In Action</h2>
        <p class="section-subtitle">Visualizing neural network activations to support transparent decision making.</p>
    </div>
    <div class="diff-visual-container animate-fade-in-up">
        <div class="diff-active-tag">
            <span class="pulse-dot"></span>
            Grad-CAM Overlay Focus Activated
        </div>
        <img class="diff-img-glow" src="data:image/png;base64,{results_b64}">
    </div>
</div>
""", unsafe_allow_html=True)

render_footer()
