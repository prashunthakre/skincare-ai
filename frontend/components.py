import base64
import streamlit as st

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

import extra_streamlit_components as stx

def get_manager():
    return stx.CookieManager(key="components_manager")

def require_login():
    # 1. Check session state first
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        return
        
    # 2. Check st.context.cookies first (completely synchronous, rerun-free)
    auth_token = None
    if hasattr(st, 'context') and hasattr(st.context, 'cookies'):
        auth_token = st.context.cookies.get('auth_token')
        
    if auth_token:
        # Restore session silently without rendering the CookieManager component
        st.session_state.logged_in = True
        st.session_state.user_name = auth_token
        return
        
    # 3. Fallback to stx CookieManager only if context cookies are not available
    cookie_manager = get_manager()
    auth_token = cookie_manager.get('auth_token')
        
    if auth_token:
        # Restore session
        st.session_state.logged_in = True
        st.session_state.user_name = auth_token
        return

    # If we still don't have the token, they are truly logged out or expired.
    try:
        st.switch_page("app.py")
    except Exception:
        st.warning("Please log in from the main page.")
        st.stop()


def render_header():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Hide default Streamlit components */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Custom Header Styling */
        .custom-navbar {
            background-color: #ffffff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.2rem 5rem;
            box-shadow: 0 4px 30px rgba(0,0,0,0.02);
            position: sticky;
            top: 0;
            z-index: 99999;
            font-family: 'Outfit', sans-serif;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .logo-section h2 {
            margin: 0;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.7rem;
            text-transform: uppercase;
        }
        
        .nav-links {
            display: flex;
            gap: 2.5rem;
            align-items: center;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #475569;
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            transition: color 0.3s ease;
            position: relative;
            font-family: 'Outfit', sans-serif;
        }
        
        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -6px;
            left: 0;
            background: linear-gradient(135deg, #0ea5e9 0%, #2dd4bf 100%);
            transition: width 0.3s ease;
        }
        
        .nav-links a:hover {
            color: #0ea5e9;
        }
        
        .nav-links a:hover::after {
            width: 100%;
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            align-items: center;
            font-family: 'Outfit', sans-serif;
        }
        
        .btn-call {
            background-color: #f1f5f9;
            color: #475569 !important;
            padding: 0.65rem 1.6rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
        }
        .btn-call:hover { background-color: #e2e8f0; transform: translateY(-1px); }
        
        .btn-book {
            background: linear-gradient(135deg, #0ea5e9 0%, #01579b 100%);
            color: white !important;
            padding: 0.65rem 1.6rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 10px;
            box-shadow: 0 8px 20px rgba(14, 165, 233, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .btn-book:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(14, 165, 233, 0.35); }
        
        .btn-logout {
            background-color: #fef2f2;
            color: #ef4444 !important;
            border: 1px solid #fecaca;
            padding: 0.65rem 1.6rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-radius: 10px;
        }
        .btn-logout:hover { background-color: #fee2e2; transform: translateY(-1px); border-color: #fca5a5; }
        
        @media (max-width: 900px) {
            .nav-links { display: none; }
            .custom-navbar { padding: 1rem 2rem; }
        }
    </style>
    
    <div class="custom-navbar">
        <div class="logo-section">
            <h2>SKINCARE AI</h2>
        </div>
        <div class="nav-links">
            <a href="/" target="_self">Home</a>
            <a href="/About_Us" target="_self">About Us</a>
            <a href="/Diagnosis" target="_self">Diagnosis</a>
            <a href="/Contact" target="_self">Contact</a>
        </div>
        <div class="nav-buttons">
            <a href="/Contact" target="_self" class="btn-call">Support</a>
            <a href="/Diagnosis" target="_self" class="btn-book">Try AI Analysis</a>
            <a href="/?logout=true" target="_self" class="btn-logout">Logout</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <style>
        .custom-footer {
            background-color: #0f172a;
            padding: 5rem 5rem 3rem 5rem;
            margin-top: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #94a3b8;
            font-size: 0.95rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
        .footer-col {
            flex: 1;
            min-width: 250px;
            margin-bottom: 2.5rem;
        }
        .footer-col h4 {
            font-family: 'Outfit', sans-serif;
            color: #f8fafc;
            margin-bottom: 1.8rem;
            font-weight: 700;
            font-size: 1.15rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .footer-col p {
            line-height: 1.8;
            margin-bottom: 0.8rem;
            font-weight: 300;
        }
        .footer-col a {
            color: #94a3b8;
            text-decoration: none;
            display: block;
            margin-bottom: 0.9rem;
            transition: all 0.3s ease;
            font-weight: 400;
        }
        .footer-col a:hover {
            color: #38bdf8;
            transform: translateX(3px);
        }
        .copyright {
            width: 100%;
            text-align: center;
            padding-top: 2.5rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 400;
        }
    </style>
    
    <div class="custom-footer">
        <div class="footer-col">
            <h4>SKINCARE AI PRO</h4>
            <p>Pioneering AI-driven Dermatology.<br>Empowering patients and professionals with instant, accurate, and explainable digital screenings.</p>
        </div>
        <div class="footer-col">
            <h4>QUICK LINKS</h4>
            <a href="/" target="_self">Home</a>
            <a href="/Diagnosis" target="_self">Try AI Diagnosis</a>
            <a href="/About_Us" target="_self">About The Technology</a>
            <a href="/Contact" target="_self">Contact Us</a>
        </div>
        <div class="footer-col">
            <h4>CONTACT CLINIC</h4>
            <p>📧 info@skincareai.com</p>
            <p>📞 +1 (800) 123-4567</p>
            <p>📍 123 Tech Valley Blvd, San Francisco, CA</p>
        </div>
        <div class="copyright">
            © 2026 SkinCare AI Pro. All rights reserved. Not a replacement for professional medical advice.
        </div>
    </div>
    """, unsafe_allow_html=True)
