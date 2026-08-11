import streamlit as st
import sys
import os
# Adjust path to import backend and components packages
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '../..')))

from components import render_header, render_footer, require_login

st.set_page_config(page_title="Contact Us | SkinCare AI Pro", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")
require_login()

render_header()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #fafbfc !important;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in-up {
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    .contact-header-section {
        text-align: center;
        padding: 5rem 2rem 4rem 2rem;
        background: radial-gradient(circle at 50% 50%, #ffffff 0%, #f8fafc 100%);
        border-bottom: 1px solid #e2e8f0;
    }
    
    .contact-header-section h1 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin: 0 0 1rem 0;
        background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .contact-container {
        display: flex;
        flex-wrap: wrap;
        max-width: 1100px;
        margin: 4rem auto;
        background: #ffffff;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.05);
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .contact-info {
        flex: 1;
        padding: 4.5rem;
        background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
        color: white;
        min-width: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .contact-info h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        margin-top: 0;
        margin-bottom: 2.5rem;
        letter-spacing: -0.5px;
    }
    
    .contact-item {
        display: flex;
        align-items: flex-start;
        gap: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .contact-item-icon {
        font-size: 1.5rem;
        background: rgba(255, 255, 255, 0.15);
        padding: 0.6rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        line-height: 1;
    }
    
    .contact-item-details strong {
        display: block;
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: rgba(255, 255, 255, 0.85);
        margin-bottom: 0.2rem;
    }
    
    .contact-item-details p {
        margin: 0;
        font-size: 1.05rem;
        color: white;
        line-height: 1.5;
        font-weight: 300;
    }
    
    .contact-form-ui {
        flex: 1.5;
        padding: 4.5rem;
        min-width: 350px;
        background: #ffffff;
    }
    
    /* Inputs styling */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.75rem 1rem !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: #0ea5e9 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
    }
    
    /* Form labels style */
    div[data-testid="stWidgetLabel"] p {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
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
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.25) !important;
        height: auto !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #0288d1 0%, #014377 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(14, 165, 233, 0.4) !important;
    }
</style>

<div class="contact-header-section animate-fade-in-up">
    <h1>Get In Touch</h1>
    <p style="color:#64748b; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; max-width: 600px; margin: 0 auto; font-weight: 400; line-height: 1.5;">
        We would love to hear from you. Please reach out with any inquiries or feedback regarding our digital dermatological tools.
    </p>
</div>

<div class="contact-container animate-fade-in-up">
    <div class="contact-info">
        <h3>Contact Details</h3>
        
        <div class="contact-item">
            <div class="contact-item-icon">📍</div>
            <div class="contact-item-details">
                <strong>Address</strong>
                <p>123 Tech Valley Blvd<br>San Francisco, CA 94105</p>
            </div>
        </div>
        
        <div class="contact-item">
            <div class="contact-item-icon">📞</div>
            <div class="contact-item-details">
                <strong>Phone</strong>
                <p>+1 (800) 123-4567</p>
            </div>
        </div>
        
        <div class="contact-item">
            <div class="contact-item-icon">📧</div>
            <div class="contact-item-details">
                <strong>Email Address</strong>
                <p>info@skincareai.com</p>
            </div>
        </div>
        
        <div class="contact-item">
            <div class="contact-item-icon">🕒</div>
            <div class="contact-item-details">
                <strong>Business Hours</strong>
                <p>Mon - Fri: 9:00 AM - 6:00 PM</p>
            </div>
        </div>
    </div>
    
    <div class="contact-form-ui">
""", unsafe_allow_html=True)

st.markdown("<h3 style='margin-top: 0; margin-bottom: 2rem; color: #0f172a; font-family: \"Outfit\", sans-serif; font-weight: 700; font-size: 1.6rem;'>SEND A MESSAGE</h3>", unsafe_allow_html=True)

c_name = st.text_input("FULL NAME", placeholder="John Doe")
c_email = st.text_input("EMAIL ADDRESS", placeholder="johndoe@example.com")
c_msg = st.text_area("MESSAGE", placeholder="How can we help you?", height=150)

if st.button("Submit Inquiry", type="primary"):
    st.success("Thank you for reaching out! A representative will contact you soon.")
    
st.markdown("</div></div>", unsafe_allow_html=True)

render_footer()
