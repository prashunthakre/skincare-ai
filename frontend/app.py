import streamlit as st
import sys
import os
# Add root path to access backend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components import get_base64_of_bin_file
from backend.auth_utils import register_user, login_user
import time
import extra_streamlit_components as stx

def get_manager():
    return stx.CookieManager(key="app_cookie_manager")

st.set_page_config(
    page_title="SkinCare AI - Login",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
# Custom Styling to match the aesthetic look
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
hero_b64 = get_base64_of_bin_file(os.path.join(assets_dir, "hero_bg.png"))

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Hide Default Components */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .block-container {{
        padding: 0rem !important;
        padding-top: 4rem !important;
        max-width: 90% !important;
        margin: 0 auto;
    }}
    
    /* Background & Font */
    body {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at 10% 20%, #f8fafc 0%, #f1f5f9 100%);
    }}
    
    /* Keyframe Animations */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .login-banner-text {{
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    
    /* Streamlit Primary Button Style */
    button[data-testid="stBaseButton-primary"] {{
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
    }}
    button[data-testid="stBaseButton-primary"]:hover {{
        background: linear-gradient(135deg, #0288d1 0%, #014377 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(14, 165, 233, 0.4) !important;
        color: white !important;
    }}
    
    /* Streamlit Secondary Button Style */
    button[data-testid="stBaseButton-secondary"] {{
        background: rgba(255, 255, 255, 0.8) !important;
        color: #475569 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: none !important;
        height: auto !important;
        padding: 0.75rem 1.5rem !important;
    }}
    button[data-testid="stBaseButton-secondary"]:hover {{
        background: #f8fafc !important;
        color: #0f172a !important;
        border-color: #94a3b8 !important;
        transform: translateY(-1px) !important;
    }}
    
    /* Center columns vertically */
    [data-testid="column"] {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 1.5rem;
    }}
    
    /* Glassmorphic Form Container */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        padding: 3rem 2.5rem !important;
    }}
    
    /* TextInput and DateInput Customizations */
    div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input {{
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.75rem 1rem !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stTextInput"] input:focus, div[data-testid="stDateInput"] input:focus {{
        border-color: #0ea5e9 !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.15) !important;
    }}
    
    /* Form Label Styling */
    div[data-testid="stWidgetLabel"] p {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }}
</style>

""", unsafe_allow_html=True)

# Application Routing based on login state
cookie_manager = get_manager()

# Handle logout from navbar
if st.query_params.get("logout") == "true":
    st.session_state.logged_in = False
    if 'user_name' in st.session_state:
        del st.session_state['user_name']
    
    try:
        cookie_manager.delete('auth_token')
    except KeyError:
        pass
        
    st.query_params.clear()

# If the user visits app.py but already has a valid session/cookie, redirect them
if st.session_state.logged_in:
    st.switch_page("pages/0_Home.py")

# --- Split Screen Layout ---
col1, space, col2 = st.columns([1.2, 0.1, 1])

# --- Banner Side ---
with col1:
    st.markdown(f"""
    <div style="background-image: url('data:image/png;base64,{hero_b64}'); background-size: cover; background-position: center; border-radius: 20px; height: 85vh; position: relative; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.1);">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, rgba(2, 136, 209, 0.85) 0%, rgba(1, 87, 155, 0.95) 100%); display: flex; flex-direction: column; justify-content: center; padding: 4rem; color: white;">
            <h1 style="font-size: 3.5rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">SKINCARE AI</h1>
            <p style="font-size: 1.2rem; font-weight: 300; line-height: 1.6; max-width: 500px; opacity: 0.95;">
                Pioneering AI-driven Dermatology. <br><br>
                Empowering patients and professionals with instant, accurate, and secure analysis.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Form Side ---
with col2:
    with st.container(border=True):        
        if 'auth_view' not in st.session_state:
            st.session_state.auth_view = 'login'
            
        if st.session_state.auth_view == 'login':
            st.markdown("<h2 style='text-align: center; font-weight: 800; font-family: \"Outfit\", sans-serif; letter-spacing: 0px; background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 2rem; font-size: 2.2rem;'>Welcome Back</h2>", unsafe_allow_html=True)
            email = st.text_input("Email ID", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In", type="primary", use_container_width=True):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating..."):
                        success, message = login_user(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_name = message 
                            st.session_state.show_welcome_popup = True
                            cookie_manager.set('auth_token', message, max_age=60*60)
                            st.success("Login Successful!")
                            time.sleep(1)
                            st.switch_page("pages/0_Home.py")
                        else:
                            st.error(message)
                            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center; color:#64748b; font-family: \"Plus Jakarta Sans\", sans-serif; font-size:0.9rem; margin-bottom:0.5rem;'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("Create an Account", type="secondary", use_container_width=True):
                 st.session_state.auth_view = 'register'
                 st.rerun()

        else:
            st.markdown("<h2 style='text-align: center; font-weight: 800; font-family: \"Outfit\", sans-serif; letter-spacing: 0px; background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 2rem; font-size: 2.2rem;'>Create Account</h2>", unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="John Doe")
            phone = st.text_input("Phone Number", placeholder="+1 234 567 890")
            dob = st.date_input("Date of Birth", min_value=None, max_value=None)
            email = st.text_input("Email ID", placeholder="johndoe@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register", type="primary", use_container_width=True):
                 if not all([name, phone, dob, email, password]):
                     st.error("Please fill in all fields.")
                 else:
                     with st.spinner("Creating account..."):
                         success, message = register_user(name, phone, dob, email, password)
                         if success:
                             st.success(message)
                             time.sleep(2)
                             st.session_state.auth_view = 'login'
                             st.rerun()
                         else:
                             st.error(message)
                             
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div style='text-align:center; color:#64748b; font-family: \"Plus Jakarta Sans\", sans-serif; font-size:0.9rem; margin-bottom:0.5rem;'>Already have an account?</div>", unsafe_allow_html=True)
            if st.button("Back to Login", type="secondary", use_container_width=True):
                 st.session_state.auth_view = 'login'
                 st.rerun()
