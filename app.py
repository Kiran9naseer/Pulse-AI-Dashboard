# =============================================================================
# app.py - Main Entry Point | AI SaaS MVP
# =============================================================================
# Purpose: Ultra-Premium $100/mo SaaS UI using heavy CSS overlays and styling.
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit_autorefresh import st_autorefresh
from database.db import init_db, create_user, login_user, add_log, get_logs
from automation.ai_reply import generate_reply
from automation.linkedin import start_posting
from automation.email_handler import send_email_alert
from automation.whatsapp import send_whatsapp_alert

# --- Initialization ---
init_db()

st.set_page_config(
    page_title="AI Pulse | Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- $100/mo SaaS Ultra-Premium Aesthetics (Linear/Vercel Vibe) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        /* Background & Root Typography */
        .stApp {
            background-color: #fafafa;
            background-image: 
                radial-gradient(circle at 10% 0%, rgba(249,115,22, 0.03) 0%, transparent 40%),
                radial-gradient(circle at 90% 100%, rgba(15,23,42, 0.02) 0%, transparent 40%);
            color: #111827;
            font-family: 'Inter', -apple-system, sans-serif;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-font-smoothing: antialiased;
        }
        
        /* Enforce Typography + Global Gentle Background */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', -apple-system, sans-serif !important;
        }
        
        .stApp {
            background: radial-gradient(circle at 50% 10%, rgba(249, 115, 22, 0.05) 0%, transparent 60%),
                        radial-gradient(circle at 10% 80%, rgba(59, 130, 246, 0.03) 0%, transparent 40%),
                        #f8fafc !important;
        }

        /* Container & Hierarchy Formatting (Restored safely for layout stability) */
        .block-container {
            padding-top: 3.5rem;
            padding-bottom: 5rem;
            animation: appFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes appFadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Elegant Headings */
        h1, h2, h3, h4 {
            color: #030712 !important;
            font-weight: 700 !important;
            letter-spacing: -0.03em;
        }
        .main-title {
            font-size: 2.5rem;
            font-weight: 800 !important;
            background: linear-gradient(180deg, #111827 0%, #374151 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
            letter-spacing: -0.04em;
        }
        .subtitle {
            font-size: 1.05rem;
            color: #6b7280;
            margin-top: 6px;
            margin-bottom: 40px;
            font-weight: 400;
            letter-spacing: -0.01em;
        }

        /* Glassmorphism Auth / Container Layering */
        .glass-card {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 24px;
            padding: 48px;
            box-shadow: 
                0 4px 6px -1px rgba(0, 0, 0, 0.02),
                0 20px 40px -10px rgba(0, 0, 0, 0.06),
                0 0 40px rgba(249, 115, 22, 0.03);
            transition: transform 0.3s ease;
        }

        /* Premium Dashboard Cards */
        .saas-card {
            background: #ffffff;
            border: 1px solid #f3f4f6;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 
                0 1px 2px rgba(0,0,0,0.02), 
                0 4px 12px rgba(0,0,0,0.02);
            transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .saas-card:hover {
            transform: scale(1.02);
            box-shadow: 
                0 4px 6px rgba(0,0,0,0.02),
                0 20px 25px -5px rgba(0,0,0,0.05),
                0 8px 10px -6px rgba(0,0,0,0.01);
            border-color: #e5e7eb;
            z-index: 5;
        }
        
        .card-header {
            font-size: 15px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            letter-spacing: -0.01em;
        }
        .card-header svg {
            margin-right: 12px;
            color: #9ca3af;
        }

        /* Highly Styled Metric Numbers */
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #030712;
            margin-top: 6px;
            letter-spacing: -0.03em;
        }
        .metric-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        /* Elegant Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 14px 20px;
            border-radius: 16px;
            font-weight: 500;
            font-size: 14px;
            width: 100%;
        }
        .badge-running {
            background: linear-gradient(90deg, #ecfdf5 0%, #f0fdf4 100%);
            color: #065f46;
            border: 1px solid #d1fae5;
            box-shadow: inset 0 1px 0 #ffffff;
        }
        .badge-stopped {
            background: linear-gradient(90deg, #fef2f2 0%, #fff1f2 100%);
            color: #991b1b;
            border: 1px solid #fee2e2;
            box-shadow: inset 0 1px 0 #ffffff;
        }
        .dot { height: 8px; width: 8px; border-radius: 50%; margin-right: 12px; }
        .dot-green { background-color: #10b981; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2); }
        .dot-red { background-color: #ef4444; box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.2); }

        /* Next-Gen Buttons with Glow */
        button[kind="primary"] {
            background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
            border: 1px solid #c2410c !important;
            box-shadow: 
                0 4px 12px rgba(249, 115, 22, 0.3), 
                inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
            border-radius: 10px !important; /* Soft premium curve */
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 14.5px !important;
            padding: 10px 20px !important;
            min-height: 44px !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            letter-spacing: -0.01em;
        }
        button[kind="primary"]:hover {
            box-shadow: 
                0 6px 20px rgba(249, 115, 22, 0.45), 
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-2px) scale(1.02);
            filter: brightness(1.05);
        }
        button[kind="primary"]:active { transform: translateY(1px) scale(0.98) !important; }
        
        button[kind="secondary"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            color: #334155 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
            font-weight: 600 !important;
            font-size: 14.5px !important;
            padding: 10px 20px !important;
            min-height: 44px !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        button[kind="secondary"]:hover {
            background: #f8fafc !important;
            border-color: #cbd5e1 !important;
            transform: translateY(-2px);
            color: #0f172a !important;
        }

        /* Rounded Alerts */
        div[data-testid="stAlert"] {
            border-radius: 16px !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
            padding: 16px 20px !important;
        }
        div[data-testid="stAlert"][data-baseweb="notification"] {
            background-color: #fef2f2 !important; /* Soft red for errors */
            color: #991b1b !important;
        }

        /* Crisp Inputs */
        div[data-baseweb="input"] {
            border-radius: 16px !important;
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.02) !important;
            transition: all 0.2s ease;
            font-size: 14px !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #ff6a00 !important;
            box-shadow: 0 0 0 3px rgba(255, 106, 0, 0.15), inset 0 1px 2px rgba(0,0,0,0.01) !important;
        }

        /* Sophisticated Timeline Logs */
        .logs-scroll { max-height: 380px; overflow-y: auto; padding: 12px 20px 12px 10px; }
        .timeline { position: relative; padding-left: 24px; margin-top: 8px; }
        .timeline::before {
            content: ''; position: absolute; left: 8px; top: 6px; bottom: 0;
            width: 2px; background-color: #f3f4f6; border-radius: 2px;
        }
        .timeline-item { position: relative; margin-bottom: 26px; animation: slideInX 0.4s ease forwards; }
        @keyframes slideInX { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        
        .timeline-dot {
            position: absolute; left: -21.5px; top: 5.5px; width: 11px; height: 11px;
            border-radius: 50%; border: 2.5px solid #ffffff; box-shadow: 0 0 0 1px #cbd5e1;
        }
        .dot-exec { background-color: #10b981; box-shadow: 0 0 0 1.5px #a7f3d0; } 
        .dot-sys { background-color: #ff6a00; box-shadow: 0 0 0 1.5px #fed7aa; }  
        
        .timeline-content {
            background: #ffffff; border: 1px solid #f1f5f9; border-radius: 16px;
            padding: 14px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            transition: all 0.2s ease;
        }
        .timeline-content:hover { border-color: #e2e8f0; box-shadow: 0 4px 8px rgba(0,0,0,0.04); background: #fdfdfd; }
        .timeline-time { font-size: 0.65rem; color: #94a3b8; margin-bottom: 6px; font-family: ui-monospace, monospace; letter-spacing: 0.05em; text-transform: uppercase; }
        .timeline-text { font-size: 0.85rem; color: #1e293b; font-weight: 500; }

        /* Ultimate Sidebar UI */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #f1f5f9;
        }
        .sidebar-logo { display:flex; align-items:center; margin-bottom: 24px; margin-top: 10px; }
        .sidebar-logo-icon {
            background: linear-gradient(135deg, #111827 0%, #374151 100%);
            color: white; width: 34px; height: 34px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 16px; margin-right: 12px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        }
        
        /* Premium User Profile Card in Sidebar */
        .user-profile-card {
            background: #ffffff;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
            margin-bottom: 12px;
            cursor: pointer;
        }
        .user-profile-card:hover {
            border-color: #d1d5db;
            background: #f9fafb;
        }
        
        /* Sidebar active item highlight */
        div[data-testid="stRadio"] > div { gap: 4px; }
        div[data-testid="stRadio"] label {
            padding: 10px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; font-weight: 500 !important; font-size: 14px !important; color: #4b5563 !important;
        }
        div[data-testid="stRadio"] label:hover { background-color: #f3f4f6; color: #111827 !important; }
        div[data-testid="stRadio"] [data-checked="true"] {
            background-color: #fff7ed !important; 
            color: #ea580c !important; 
            font-weight: 600 !important;
            box-shadow: inset 3px 0 0 #f97316;
            border-radius: 4px 8px 8px 4px;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
    </style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INIT
# =============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "automation_running" not in st.session_state:
    st.session_state.automation_running = False

if "pref_linkedin" not in st.session_state:
    st.session_state.pref_linkedin = True
if "pref_email" not in st.session_state:
    st.session_state.pref_email = True
if "pref_whatsapp" not in st.session_state:
    st.session_state.pref_whatsapp = True


# =============================================================================
# UNAUTHENTICATED VIEW -> Centered Login with Columns (NO CSS Hack)
# =============================================================================
if not st.session_state.logged_in:

    st.markdown("""
        <style>
            section[data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
            @keyframes loginFadeUp {
                from { opacity: 0; transform: translateY(12px); }
                to   { opacity: 1; transform: translateY(0); }
            }
            .login-card {
                background: rgba(255,255,255,0.85);
                padding: 36px 32px 28px 32px;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.12);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255,255,255,0.5);
                animation: loginFadeUp 0.55s cubic-bezier(0.16,1,0.3,1) both;
            }
            div[data-baseweb="input"] {
                border-radius: 10px !important;
                border: 1px solid #e2e8f0 !important;
                background: #ffffff !important;
                transition: all 0.2s ease;
            }
            div[data-baseweb="input"]:focus-within {
                border-color: #f97316 !important;
                box-shadow: 0 0 0 3px rgba(249,115,22,0.15) !important;
            }
            .divider { display:flex; align-items:center; color:#9ca3af; font-size:13px; margin:20px 0; }
            .divider::before, .divider::after { content:''; flex:1; border-bottom:1px solid #e5e7eb; }
            .divider:not(:empty)::before { margin-right:.5em; }
            .divider:not(:empty)::after  { margin-left:.5em; }
            .forgot-link { display:block; text-align:right; font-size:12.5px; color:#f97316; text-decoration:none; margin-top:-8px; margin-bottom:14px; font-weight:500; }
            .forgot-link:hover { color:#ea580c; text-decoration:underline; }
            div.stButton > button {
                background-color: #F97316;
                color: white;
                border-radius: 999px;
                height: 48px;
                width: 100%;
                font-weight: 600;
                border: none;
                transition: all 0.2s ease;
            }
            div.stButton > button:hover {
                background-color: #ea580c;
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(249,115,22,0.35);
            }
        </style>
    """, unsafe_allow_html=True)

    # ── Centered 3-column layout ──────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("<h1 style='text-align:center; color:#1F2937;'>Pulse.ai</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#6B7280;'>Smart AI Automation Dashboard</p>", unsafe_allow_html=True)

        st.markdown("""
            <div style="
                background:#FFFFFF;
                padding:30px;
                border-radius:16px;
                border:1px solid #E5E7EB;
                box-shadow:0 4px 12px rgba(0,0,0,0.05);
            ">
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.write("")
            with st.form("login_form"):
                login_username = st.text_input("Work Email", placeholder="name@company.com")
                login_password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign in →", type="primary", use_container_width=True)

            if submitted:
                if not login_username or not login_password:
                    st.warning("Please fill in both fields.")
                elif login_user(login_username, login_password):
                    st.session_state.logged_in = True
                    st.session_state.current_user = login_username
                    add_log(f"[SYS] User '{login_username}' authenticated successfully.")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with tab_signup:
            st.write("")
            with st.form("signup_form"):
                signup_username = st.text_input("Full Name or Email", placeholder="Jane Doe")
                signup_password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
                signup_confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                st.write("")
                submitted_signup = st.form_submit_button("Create account →", type="primary", use_container_width=True)

            if submitted_signup:
                if signup_password != signup_confirm:
                    st.error("Passwords do not match.")
                else:
                    if create_user(signup_username, signup_password):
                        st.success("Account created! Please sign in.")
                        add_log(f"[SYS] New tenant provisioned: '{signup_username}'")
                    else:
                        st.error("Username already taken.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.button("Continue with SSO", use_container_width=True)



# =============================================================================
# LOGGED IN VIEW -> Enterprise Dashboard
# =============================================================================
else:
    
    # Build Analytics
    logs = get_logs(limit=200)
    total_runs = len(logs)
    errors_today = sum(1 for l in logs if "Error" in l['message'] or "NotFound" in l['message'])
    success_rate = 100 if total_runs == 0 else int(((total_runs - errors_today) / total_runs) * 100)
    active_flows = sum([st.session_state.pref_linkedin, st.session_state.pref_email, st.session_state.pref_whatsapp])

    # Dynamic Smooth Curve Data (Line chart native)
    chart_data = pd.DataFrame(
        np.abs(np.cumsum(np.random.randn(20, 2) * 2 + 1, axis=0)) + 10,
        columns=['Inbound', 'Processed']
    )

    # -------------------------------------------------------------------------
    # FIXED SIDEBAR
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-logo">
                <div class="sidebar-logo-icon">
                    <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
                <div style="font-weight: 800; font-size: 19px; color:#030712; letter-spacing:-0.03em;">Pulse.ai</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        
        page = st.radio(
            "Main Menu",
            ["📊 Pipeline Dashboard", "🧠 Inference Engine", "⚙️ Integrations"],
            label_visibility="collapsed"
        )
        
        st.write("---")
        
        # Premium User Profile Card
        st.markdown(f"""
            <div class='user-profile-card'>
                <div style='width:36px; height:36px; border-radius: 8px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); display:flex; align-items:center; justify-content:center; margin-right: 12px; font-weight:700; color:#334155; border: 1px solid #cbd5e1;'>
                    {st.session_state.current_user[0].upper()}
                </div>
                <div style='flex-grow: 1;'>
                    <div style='font-size:13px; font-weight: 600; color:#111827; letter-spacing:-0.01em;'>{st.session_state.current_user}</div>
                    <div style='font-size:11px; color:#6b7280; font-weight: 500;'>Enterprise Plan</div>
                </div>
                <div style='color: #9ca3af;'>
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign out", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.automation_running = False
            add_log("[SYS] User session terminated.")
            st.rerun()

    # -------------------------------------------------------------------------
    # MAIN WORKSPACE
    # -------------------------------------------------------------------------
    if page == "📊 Pipeline Dashboard":
        
        st.markdown("<h1 class='main-title'>Infrastructure Overview</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Monitor throughput, system health, and orchestrate environments.</p>", unsafe_allow_html=True)
        
        # 1. TOP STATS CARDS
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">Total Volume</div><div class="metric-value">{total_runs + 2042}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">Active Endpoints</div><div class="metric-value">{active_flows}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">System Uptime</div><div class="metric-value" style="color: #10b981;">{success_rate}%</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">Caught Errrors</div><div class="metric-value" style="color: #ef4444;">{errors_today}</div></div>', unsafe_allow_html=True)

        
        # 2. STATUS + ACTIONS 
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown("""
            <div class='card-header'>
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                Core Engine State
            </div>
        """, unsafe_allow_html=True)
        
        stat_col, action_col = st.columns([1.5, 1], gap="medium")
        
        with stat_col:
            if st.session_state.automation_running:
                st.markdown("""
                    <div class="status-badge badge-running">
                        <span class="dot dot-green"></span>
                        <div style="flex-grow: 1;">Orchestration Active — Processing Queues</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="status-badge badge-stopped">
                        <span class="dot dot-red"></span>
                        <div style="flex-grow: 1;">Engine Paused — Workflows Suspended</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<p style='font-size: 13px; color: #6b7280; margin-top: 12px;'>Control the primary event loop. Background triggers will queue safely until the system resumes.</p>", unsafe_allow_html=True)

        with action_col:
            st.write("")
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Engage Node ⚡", type="primary", disabled=st.session_state.automation_running, use_container_width=True):
                    st.session_state.automation_running = True
                    add_log(f"[SYS] Execution thread enabled.")
                    if st.session_state.pref_linkedin: start_posting()
                    if st.session_state.pref_email: send_email_alert("admin@example.com")
                    if st.session_state.pref_whatsapp: send_whatsapp_alert("+1234567890")
                    st.rerun()
            with b2:
                if st.button("Halt Node 🛑", type="secondary", disabled=not st.session_state.automation_running, use_container_width=True):
                    st.session_state.automation_running = False
                    add_log(f"[SYS] Execution thread halted.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


        # 3. MIDDLE TIER - CHART & TOGGLES
        mid_col1, mid_col2 = st.columns([2, 1], gap="large")
        
        with mid_col1:
            st.markdown('<div class="saas-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<div class='card-header'>Performance Analytics</div>", unsafe_allow_html=True)
            
            # Smooth Altair Area Chart satisfying explicit 'Smooth Curve, Custom gradient' constraints
            chart = alt.Chart(chart_data.reset_index().melt('index', var_name='Type', value_name='Volume')).mark_area(
                line=True, interpolate='monotone', opacity=0.7
            ).encode(
                x=alt.X('index', axis=alt.Axis(grid=False, labels=False, ticks=False, title=None)),
                y=alt.Y('Volume', axis=alt.Axis(grid=True, gridColor='#f1f5f9', title=None)),
                color=alt.Color('Type', scale=alt.Scale(range=['#ff6a00', '#3b82f6']), legend=None),
                tooltip=['Type', 'Volume']
            ).configure_view(strokeWidth=0)
            st.altair_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with mid_col2:
            st.markdown('<div class="saas-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<div class='card-header'>Webhooks & Integrations</div>", unsafe_allow_html=True)
            st.toggle("LinkedIn Graph API", key="pref_linkedin", disabled=st.session_state.automation_running)
            st.toggle("SES Email Relay", key="pref_email", disabled=st.session_state.automation_running)
            st.toggle("WhatsApp Cloud API", key="pref_whatsapp", disabled=st.session_state.automation_running)
            st.markdown('</div>', unsafe_allow_html=True)


        # 4. TIMELINE ACTIVITY LOGS
        st.markdown('<div class="saas-card" style="margin-bottom: 0px;">', unsafe_allow_html=True)
        st.markdown("""
            <div class='card-header'>
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
                System Traces & Execution Logs
            </div>
        """, unsafe_allow_html=True)
        
        st_autorefresh(interval=5000, key="log_autorefresh")
        display_logs = get_logs(limit=40)
        
        if not display_logs:
            st.markdown("<p style='color:#9ca3af; font-size:14px; text-align:center; padding: 30px;'>Awaiting system events...</p>", unsafe_allow_html=True)
        else:
            html_logs = '<div class="logs-scroll"><div class="timeline">'
            for log in display_logs:
                msg = log['message']
                
                # Determine node type relative mapping
                is_err = "Error" in msg or "Fail" in msg or "404" in msg
                is_exec = "[EXEC]" in msg
                
                if is_err: dot_class = "dot-err"
                elif is_exec: dot_class = "dot-exec"
                else: dot_class = "dot-sys"
                
                clean_msg = msg.replace("[EXEC] ", "").replace("[SYS] ", "")
                
                html_logs += f"<div class='timeline-item'><div class='timeline-dot {dot_class}'></div><div class='timeline-content'><div class='timeline-time'>{log['timestamp']}</div><div class='timeline-text'>{clean_msg}</div></div></div>"
                
            html_logs += '</div></div>'
            st.markdown(html_logs, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)


    # -------------------------------------------------------------------------
    # AI PLAYGROUND 
    # -------------------------------------------------------------------------
    elif page == "🧠 Inference Engine":
        st.markdown("<h1 class='main-title'>Model Sandbox</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Test standard generations manually in isolation.</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown("<div class='card-header'>Direct LLM Interface</div>", unsafe_allow_html=True)
        
        user_message = st.text_area("Input Context", placeholder="Type a prompt to test your logic...", height=120)
        st.write("")
        
        if st.button("Generate Output", type="primary"):
            if not user_message:
                st.warning("Payload empty.")
            else:
                with st.spinner("Processing neural weights..."):
                    ai_response = generate_reply(user_message)
                    add_log(f"[SYS] Sandbox generation executed.")
                    
                    st.markdown("---")
                    st.markdown("<div style='font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Target Response</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='background: #f8fafc; border: 1px solid #e5e7eb; padding: 20px; border-radius: 12px; font-size: 14px; color: #1e293b; line-height: 1.6;'>{ai_response}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SETTINGS PLACEHOLDER
    # -------------------------------------------------------------------------
    elif page == "⚙️ Integrations":
        st.markdown("<h1 class='main-title'>Settings & Integrations</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Manage credentials and webhooks.</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown("<div class='card-header'>Environment Keys</div>", unsafe_allow_html=True)
        st.write("Configuration options will interface with your .env schema here.")
        st.markdown('</div>', unsafe_allow_html=True)
