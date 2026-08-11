import streamlit as st
import sys
import os
# Adjust path to import backend and components packages
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '../..')))

from components import render_header, render_footer, get_base64_of_bin_file, require_login

st.set_page_config(page_title="About Us | SkinCare AI Pro", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")
require_login()

render_header()

assets_dir = os.path.abspath(os.path.join(current_dir, "..", "assets"))
hero_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "about_clinic.png"))

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    body {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #fafbfc !important;
    }}
    
    /* Animations */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .animate-fade-in-up {{
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    
    .animation-delay-1 {{
        animation-delay: 0.15s;
        opacity: 0;
    }}
    .animation-delay-2 {{
        animation-delay: 0.3s;
        opacity: 0;
    }}
    
    /* Hero Banner */
    .about-hero {{
        height: 60vh;
        min-height: 400px;
        background-image: url('data:image/png;base64,{hero_b64}');
        background-size: cover;
        background-position: center;
        border-radius: 0 0 40px 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.05);
    }}
    
    .hero-overlay-gradient {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.8) 0%, rgba(1, 87, 155, 0.9) 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        color: white;
    }}
    
    .hero-title {{
        font-family: 'Outfit', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0 0 1rem 0;
        text-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    .hero-subtitle {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.25rem;
        font-weight: 300;
        max-width: 600px;
        margin: 0;
        opacity: 0.95;
    }}
    
    /* Content Layout */
    .about-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2.5rem;
        max-width: 1200px;
        margin: -50px auto 6rem auto;
        padding: 0 2rem;
        position: relative;
        z-index: 10;
    }}
    
    .about-card {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.06);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: center;
    }}
    
    .about-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.12);
        border-color: rgba(14, 165, 233, 0.3);
    }}
    
    .about-icon {{
        font-size: 2.8rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        background: #f0fdfa;
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid #ccfbf1;
    }}
    
    /* Alternate icon background for visual rhythm */
    .about-card:nth-child(2) .about-icon {{
        background: #f0f9ff;
        border-color: #e0f2fe;
    }}
    .about-card:nth-child(3) .about-icon {{
        background: #faf5ff;
        border-color: #f3e8ff;
    }}
    
    .card-title {{
        font-family: 'Outfit', sans-serif;
        color: #0f172a;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 0;
        margin-bottom: 1.2rem;
    }}
    
    .card-text {{
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.75;
        margin: 0;
        font-weight: 400;
    }}
</style>

<div class="about-hero animate-fade-in-up">
    <div class="hero-overlay-gradient">
        <h1 class="hero-title">Pioneering Digital Health</h1>
        <p class="hero-subtitle">The Story and Tech Behind SkinCare AI Pro</p>
    </div>
</div>

<div class="about-container">
    <div class="about-card animate-fade-in-up shadow-sm">
        <div class="about-icon">🩺</div>
        <h3 class="card-title">Our Story</h3>
        <p class="card-text">
            <strong>SkinCare AI Pro</strong> was founded by a team of forward-thinking dermatologists and rigorous AI engineers. 
            Our goal is to bridge the gap between advanced medical technology and everyday patient care, putting clinical-grade diagnostic power in your hands.
        </p>
    </div>
    
    <div class="about-card animate-fade-in-up shadow-sm animation-delay-1">
        <div class="about-icon">🧠</div>
        <h3 class="card-title">The Technology</h3>
        <p class="card-text">
            We leverage cutting-edge Deep Learning convolutional neural network architectures, trained extensively on the verified 
            HAM10000 clinical dataset. This enables highly accurate multi-class classification of complex skin lesions in seconds.
        </p>
    </div>
    
    <div class="about-card animate-fade-in-up shadow-sm animation-delay-2">
        <div class="about-icon">👁️</div>
        <h3 class="card-title">Our Commitment</h3>
        <p class="card-text">
            We are fully committed to explainable, transparent AI. By generating real-time Grad-CAM heatmaps, patients and 
            practitioners can physically see what features the neural network is analyzing, fostering trust and absolute transparency.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

render_footer()
