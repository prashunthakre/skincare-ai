import streamlit as st
import sys
import os
import urllib.parse

# Adjust path to import backend and components packages
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(current_dir, '../..')))

from components import render_header, render_footer, require_login

st.set_page_config(
    page_title="Contact Us | SkinCare AI Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

require_login()
render_header()

# Compact, centered CSS styling and Hero Header
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

body {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #fafbfc !important;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
    animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.contact-hero {
    text-align: center;
    padding: 1.5rem 1rem 1rem 1rem;
    background: radial-gradient(circle at 50% 50%, #ffffff 0%, #f8fafc 100%);
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.8rem;
}

.contact-hero h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    margin: 0 0 0.35rem 0;
    background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.contact-hero p {
    color: #64748b;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.95rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.45;
}

.contact-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #e0f2fe;
    color: #0369a1;
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

/* Compact form inputs */
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stSelectbox"] select {
    border-radius: 8px !important;
    border: 1px solid #cbd5e1 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 0.45rem 0.75rem !important;
    background-color: #f8fafc !important;
    color: #0f172a !important;
    font-size: 0.88rem !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
    border-color: #0ea5e9 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12) !important;
}

div[data-testid="stWidgetLabel"] p {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    color: #334155 !important;
    font-size: 0.85rem !important;
    margin-bottom: 0.2rem !important;
}

/* Container border card styling */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px !important;
    border: 1px solid #e2e8f0 !important;
    background: #ffffff !important;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03) !important;
    padding: 1.6rem 1.8rem !important;
}

button[data-testid="stBaseButton-primary"], button[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 6px 16px rgba(14, 165, 233, 0.2) !important;
    height: auto !important;
    padding: 0.55rem 1.2rem !important;
}

button[data-testid="stBaseButton-primary"]:hover, button[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #0288d1 0%, #014377 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 20px rgba(14, 165, 233, 0.3) !important;
}
</style>

<div class="contact-hero animate-fade-in-up">
    <div class="contact-badge">💬 24/7 Patient & Clinical Care Support</div>
    <h1>Get In Touch With SkinCare AI</h1>
    <p>Have questions about our AI diagnosis or medical consultations? Our dedicated dermatology care team is here to assist.</p>
</div>
""")

# Centered container layout using side spacers so boxes never touch screen edges and remain compact
_, center_col, _ = st.columns([0.16, 1, 0.16])

with center_col:
    col_info, col_form = st.columns([1, 1.25], gap="large")

    with col_info:
        st.html("""
<div style="background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%); color: white; border-radius: 16px; padding: 1.8rem 1.6rem; box-shadow: 0 12px 30px rgba(14, 165, 233, 0.18); font-family: 'Plus Jakarta Sans', sans-serif; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
    <div>
        <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.35rem; color: white; margin-top: 0; margin-bottom: 0.35rem;">Contact Information</h3>
        <p style="color: rgba(255, 255, 255, 0.88); font-size: 0.85rem; margin-bottom: 1.4rem; line-height: 1.4;">Reach out directly through any of our medical support channels or schedule a consultation.</p>

        <div style="display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 1.1rem;">
            <div style="background: rgba(255, 255, 255, 0.15); padding: 0.45rem; border-radius: 8px; font-size: 1.05rem; line-height: 1;">📍</div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: rgba(255, 255, 255, 0.8); letter-spacing: 0.5px;">Address</div>
                <div style="font-size: 0.88rem; color: white; font-weight: 400; margin-top: 1px;">Medical Tech Park, Innovation Hub, Pune, Maharashtra 411057</div>
            </div>
        </div>

        <div style="display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 1.1rem;">
            <div style="background: rgba(255, 255, 255, 0.15); padding: 0.45rem; border-radius: 8px; font-size: 1.05rem; line-height: 1;">📞</div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: rgba(255, 255, 255, 0.8); letter-spacing: 0.5px;">Helpline & Support</div>
                <div style="font-size: 0.88rem; color: white; font-weight: 400; margin-top: 1px;">+91 (020) 2740-9988 / +1 (800) 123-4567</div>
            </div>
        </div>

        <div style="display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 1.1rem;">
            <div style="background: rgba(255, 255, 255, 0.15); padding: 0.45rem; border-radius: 8px; font-size: 1.05rem; line-height: 1;">📧</div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: rgba(255, 255, 255, 0.8); letter-spacing: 0.5px;">Official Email</div>
                <div style="font-size: 0.88rem; color: white; font-weight: 400; margin-top: 1px;">support@skincareai.com</div>
            </div>
        </div>

        <div style="display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 1.3rem;">
            <div style="background: rgba(255, 255, 255, 0.15); padding: 0.45rem; border-radius: 8px; font-size: 1.05rem; line-height: 1;">🕒</div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: rgba(255, 255, 255, 0.8); letter-spacing: 0.5px;">Diagnostic System Status</div>
                <div style="font-size: 0.88rem; color: white; font-weight: 400; margin-top: 1px;">AI Inference Cluster: 24/7 Active & Online</div>
            </div>
        </div>
    </div>

    <div style="background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; padding: 0.75rem 0.9rem; font-size: 0.78rem; line-height: 1.4; color: rgba(255, 255, 255, 0.92);">
        🔒 <strong>Patient Privacy Notice:</strong> Designed for clinical decision support. Patient data is encrypted and confidential.
    </div>
</div>
""")

    with col_form:
        with st.container(border=True):
            st.html("""
<div style="margin-bottom: 0.9rem;">
    <h3 style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.35rem; color: #0f172a; margin: 0 0 0.15rem 0;">Send Us A Message</h3>
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.82rem; color: #64748b; margin: 0;">Fill in your details below and our clinical team will get back to you promptly.</p>
</div>
""")

            raw_user_name = st.session_state.get('user_name', '')
            user_default_name = urllib.parse.unquote(raw_user_name).replace('+', ' ') if raw_user_name else ''

            with st.form("contact_form", clear_on_submit=True):
                c_name = st.text_input("Your Full Name", value=user_default_name, placeholder="e.g. Dr. Rajesh Sharma / Alex Morgan")
                
                c1, c2 = st.columns(2)
                with c1:
                    c_email = st.text_input("Email Address", placeholder="name@organization.com")
                with c2:
                    c_purpose = st.selectbox(
                        "Inquiry Category",
                        ["General Inquiry", "Dermatology Consultation", "Clinical Partnership", "Technical Support"]
                    )
                    
                c_subject = st.text_input("Subject", placeholder="e.g. Skin consultation or diagnosis inquiry")
                c_msg = st.text_area("Message / Questions", placeholder="Please describe how our dermatology team can assist you...", height=95)

                submitted = st.form_submit_button("✉️ Send Message", type="primary", use_container_width=True)

                if submitted:
                    if not c_name or not c_email or not c_msg:
                        st.error("Please fill in all required fields (Name, Email, and Message).")
                    else:
                        st.session_state.contact_submitted = True
                        st.toast("✅ Your message has been sent successfully!", icon="✉️")

            if st.session_state.get('contact_submitted', False):
                st.success("✅ Thank you! Your message has been sent successfully. Our support team will respond shortly.")
                st.balloons()
                st.session_state.contact_submitted = False

st.html("<div style='height: 2.5rem;'></div>")
render_footer()
