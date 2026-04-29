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

st.set_page_config(
    page_title="AI SaaS",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Initialization ---
init_db()

# --- $100/mo SaaS Ultra-Premium Aesthetics (Linear/Vercel Vibe) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        /* Dashboard Design System Variables */
        :root {
            --primary: #F97316;
            --primary-hover: #FB923C;
            --bg-page: #FDFDFD;
            --bg-nav-inactive: #F8F7F5;
            --text-main: #111827;
            --text-sub: #4B5563;
            --border: #E5E7EB;
            --shadow-card: 0 4px 12px rgba(0,0,0,0.05);
            --shadow-active: 0 10px 15px -3px rgba(249,115,22, 0.25);
            --font-outfit: 'Outfit', sans-serif;
        }

        /* Global Font Application */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"], .main-title, .subtitle {
            font-family: var(--font-outfit) !important;
        }

        /* 5. Logs UI Improvements */
        .logs-container {
            max-height: 300px;
            overflow-y: auto;
            padding-right: 10px;
        }

        .log-entry-card {
            background: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            margin-bottom: 10px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            transition: border-color 0.2s ease;
        }

        .log-entry-card:hover { border-color: #D1D5DB !important; }

        .log-timestamp {
            font-size: 11px !important;
            color: #6B7280;
            font-family: ui-monospace, monospace;
            margin-bottom: 4px;
            font-weight: 500;
        }

        .log-text {
            font-size: 13.5px !important;
            font-weight: 500 !important;
            color: #1F2937;
            line-height: 1.4;
        }

        .status-pill {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 4px;
        }
        .status-enabled { background: #D1FAE5; color: #065F46; }
        .status-halted { background: #FEE2E2; color: #991B1B; }
        .status-executed { background: #FFEDD5; color: #9A3412; }

        /* Custom Scrollbar & Aesthetics */
        .stApp {
            background-color: var(--bg-page);
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: var(--text-main);
        }

        /* 1. Centered Workspace & Spacing */
        .block-container {
            max-width: 900px !important;
            padding-top: 2rem !important;
            padding-bottom: 6rem !important;
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* 2. Heading Improvements */
        h1.main-title {
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            color: #1F2937 !important;
            letter-spacing: -0.04em !important;
            margin-bottom: 24px !important;
            line-height: 1.1 !important;
        }

        p.subtitle {
            font-size: 1.15rem !important;
            color: var(--text-sub) !important;
            margin-bottom: 40px !important;
            letter-spacing: -0.01em !important;
        }

        /* 3. Premium Buttons UI */
        div.stButton > button {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border-radius: 999px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            height: auto !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%) !important;
            color: var(--text-main) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }

        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #F3F4F6 100%) !important;
            box-shadow: 0 6px 15px -3px rgba(0,0,0,0.1) !important;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 14px 0 rgba(249,115,22, 0.39) !important;
        }
        
        div.stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%) !important;
            box-shadow: 0 8px 22px rgba(249,115,22, 0.45) !important;
            transform: translateY(-2px) !important;
        }

        /* 3.1 Custom Flex Navbar */
        .navbar {
            display: flex;
            justify-content: center;
            gap: 20px;
        }

        /* 4. Infrastructure Cards Refinement */
        .saas-card {
            background: #FFFFFF !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            padding: 30px !important;
            box-shadow: var(--shadow-card) !important;
            transition: all 0.3s ease;
            margin-bottom: 30px !important;
        }

        .saas-card:hover {
            box-shadow: 0 12px 30px -10px rgba(0,0,0,0.08) !important;
            transform: translateY(-2px);
        }

        /* Metric Detail Styling */
        .metric-label {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: var(--text-sub) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-bottom: 6px;
        }
        .metric-value {
            font-size: 32px !important;
            font-weight: 800 !important;
            color: #1F2937 !important;
            letter-spacing: -0.02em !important;
        }

        /* Sidebar UI */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #f1f5f9;
        }
        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        .sidebar-logo-icon {
            background: var(--primary);
            color: white;
            padding: 8px;
            border-radius: 10px;
            display: flex;
        }
        .user-profile-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 12px;
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }

        /* 5. Logs UI Improvements */
        .logs-container {
            max-height: 300px;
            overflow-y: auto;
            padding-right: 10px;
        }

        .log-entry-card {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #E5E7EB !important;
            border-left: 4px solid #F97316 !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
            transition: all 0.3s ease !important;
            text-align: left !important;
            backdrop-filter: blur(8px);
        }

        .log-entry-card:hover { 
            transform: translateX(4px) !important;
            border-color: #D1D5DB !important; 
            box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important;
        }

        .log-timestamp {
            font-size: 11px !important;
            color: #6B7280;
            font-family: ui-monospace, monospace;
            margin-bottom: 4px;
            font-weight: 500;
        }

        .log-text {
            font-size: 13.5px !important;
            font-weight: 500 !important;
            color: #1F2937;
            line-height: 1.4;
        }

        .status-pill {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 4px;
        }
        .status-enabled { background: #D1FAE5 !important; color: #065F46 !important; }
        .status-halted { background: #FEE2E2 !important; color: #991B1B !important; }
        .status-executed { background: #FFEDD5 !important; color: #9A3412 !important; }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 10px; }

        /* Hide Streamlit branding but KEEP sidebar toggle */
        footer, .stDeployButton, 
        [data-testid="stToolbar"], [data-testid="stDecoration"],
        [data-testid="stStatusWidget"], [data-testid="stAppDeployButton"],
        .viewerBadge_container__1QSob, .viewerBadge_link__1S137 {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Specific header cleaning without hiding toggle */
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
        }
        
        /* Make sidebar wider and more professional */
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Force Sidebar State via query params or config is better, 
# but we'll stick to a robust layout.



# =============================================================================
# SESSION STATE INIT
# =============================================================================
if "page" not in st.session_state:
    st.session_state.page = "📊 Pipeline Dashboard"
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
                background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
                color: white;
                border-radius: 999px;
                height: 52px;
                width: 100%;
                font-weight: 600;
                font-size: 15px;
                border: none;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 4px 14px 0 rgba(249,115,22, 0.39);
            }
            div.stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(249,115,22,0.45);
                background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%);
            }
        </style>
    """, unsafe_allow_html=True)

    # ── Centered 3-column layout ──────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # Added Branding to Login Page
        st.markdown("""
            <div style="text-align:center; margin-bottom:20px;">
                <div style="display:inline-flex; align-items:center; justify-content:center; background:#F97316; color:white; padding:12px; border-radius:14px; margin-bottom:15px; box-shadow: 0 10px 15px -3px rgba(249,115,22, 0.3);">
                    <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
                <h1 style='color:#111827; margin-bottom:0px; font-family: "Outfit", sans-serif; font-weight:800; letter-spacing:-0.05em;'>Pulse.ai</h1>
                <p style='color:#64748B; font-family: "Outfit", sans-serif; font-weight:500; font-size:15px;'>Smart AI Automation Dashboard</p>
            </div>
        """, unsafe_allow_html=True)

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
    
    # 1. SIDEBAR FIRST (Best practice for Streamlit layout stability)
    with st.sidebar:
        st.markdown(f"""
            <div class="sidebar-logo">
                <div class="sidebar-logo-icon">
                    <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                </div>
                <div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 24px; color:#0f172a; letter-spacing:-0.04em;">Pulse.ai</div>
            </div>
            <div style="margin-bottom: 20px;"></div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        
        # Profile Card
        st.markdown(f"""
            <div class='user-profile-card'>
                <div style='width:40px; height:40px; border-radius: 10px; background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%); display:flex; align-items:center; justify-content:center; margin-right: 12px; font-weight:800; color:#1e293b; border: 1px solid #94a3b8; font-size: 16px;'>
                    {st.session_state.current_user[0].upper()}
                </div>
                <div style='flex-grow: 1;'>
                    <div style='font-size:14px; font-weight: 700; color:#111827;'>{st.session_state.current_user.split('@')[0].capitalize()}</div>
                    <div style='font-size:11px; color:#64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;'>Enterprise Client</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign out", type="secondary", use_container_width=True, key="signout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.automation_running = False
            add_log("[SYS] User session terminated.")
            st.rerun()

    # Build Analytics
    logs = get_logs(limit=200)
    total_runs = len(logs)
    errors_today = sum(1 for l in logs if "Error" in l['message'] or "NotFound" in l['message'])
    success_rate = 100 if total_runs == 0 else int(((total_runs - errors_today) / total_runs) * 100)
    active_flows = sum([st.session_state.get('pref_linkedin', True), st.session_state.get('pref_email', True), st.session_state.get('pref_whatsapp', True)])

    # Dynamic Smooth Curve Data (Line chart native)
    chart_data = pd.DataFrame(
        np.abs(np.cumsum(np.random.randn(20, 2) * 2 + 1, axis=0)) + 10,
        columns=['Inbound', 'Processed']
    )

    # -------------------------------------------------------------------------
    # MAIN WORKSPACE
    # -------------------------------------------------------------------------
    # TOP NAVIGATION MENU (Inside Main Page to avoid Sidebar bugs)
    # Navbar Spacing
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
    
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.page == "📊 Pipeline Dashboard" else "secondary"):
            st.session_state.page = "📊 Pipeline Dashboard"
            st.rerun()
    with col_nav2:
        if st.button("🧠 AI Engine", use_container_width=True, type="primary" if st.session_state.page == "🧠 Inference Engine" else "secondary"):
            st.session_state.page = "🧠 Inference Engine"
            st.rerun()
    with col_nav3:
        if st.button("⚙️ Integrations", use_container_width=True, type="primary" if st.session_state.page == "⚙️ Integrations" else "secondary"):
            st.session_state.page = "⚙️ Integrations"
            st.rerun()

    # Content Spacing
    st.markdown("<div style='margin-bottom: 35px;'></div>", unsafe_allow_html=True)
    
    page = st.session_state.page

    # -------------------------------------------------------------------------
    # MAIN WORKSPACE
    # -------------------------------------------------------------------------
    if page == "📊 Pipeline Dashboard":
        
        st.markdown("<h1 class='main-title'>Infrastructure Overview</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Monitor throughput, system health, and orchestrate environments.</p>", unsafe_allow_html=True)
        
        # 1. TOP STATS CARDS
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">Total Volume</div><div class="metric-value">{total_runs}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">Active Endpoints</div><div class="metric-value">{active_flows}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">System Uptime</div><div class="metric-value" style="color: #10b981;">{success_rate}%</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="saas-card" style="padding: 20px;"><div class="metric-label">Caught Errrors</div><div class="metric-value" style="color: #ef4444;">{errors_today}</div></div>', unsafe_allow_html=True)

        
        # 2. STATUS + ACTIONS 
        st.markdown("""
            <div style='font-size: 1.1rem; font-weight: 700; display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
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
                if st.button("Engage ⚡", type="primary", disabled=st.session_state.automation_running, use_container_width=True):
                    st.session_state.automation_running = True
                    add_log(f"[SYS] Execution thread enabled.")
                    if st.session_state.pref_linkedin: start_posting()
                    if st.session_state.pref_email: send_email_alert("admin@example.com")
                    if st.session_state.pref_whatsapp: send_whatsapp_alert("+1234567890")
                    st.rerun()
            with b2:
                if st.button("Halt 🛑", type="secondary", disabled=not st.session_state.automation_running, use_container_width=True):
                    st.session_state.automation_running = False
                    add_log(f"[SYS] Execution thread halted.")
        st.write("")

        # 3. MIDDLE TIER - CHART & TOGGLES
        mid_col1, mid_col2 = st.columns([2, 1], gap="large")
        
        with mid_col1:
            st.markdown("<div style='font-size: 1rem; font-weight: 700; margin-bottom: 12px;'>Performance Analytics</div>", unsafe_allow_html=True)
            
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
            
        with mid_col2:
            st.markdown("<div style='font-size: 1rem; font-weight: 700; margin-bottom: 12px;'>Webhooks & Integrations</div>", unsafe_allow_html=True)
            st.toggle("LinkedIn Graph API", key="pref_linkedin", disabled=st.session_state.automation_running)
            st.toggle("SES Email Relay", key="pref_email", disabled=st.session_state.automation_running)
            st.toggle("WhatsApp Cloud API", key="pref_whatsapp", disabled=st.session_state.automation_running)


        # 4. TIMELINE ACTIVITY LOGS
        st.markdown("""
            <div style='font-size: 1.1rem; font-weight: 700; display: flex; align-items: center; gap: 8px; margin-bottom: 12px;'>
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
                System Traces & Execution Logs
            </div>
        """, unsafe_allow_html=True)
        
        st_autorefresh(interval=5000, key="log_autorefresh")
        display_logs = get_logs(limit=40)
        
        if not display_logs:
            empty_state_html = """
<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 40px 20px; background: linear-gradient(180deg, rgba(248, 250, 252, 0) 0%, rgba(248, 250, 252, 0.8) 100%); border-radius: 12px; margin-top: 10px;">
    <div style="font-size: 3rem; margin-bottom: 12px; animation: pulseFade 2.5s infinite ease-in-out;">🛡️</div>
    <div style="font-size: 15px; font-weight: 600; color: #475569; margin-bottom: 6px;">AI is actively listening...</div>
    <div style="font-size: 13px; color: #94a3b8; text-align: center; max-width: 280px;">Awaiting external triggers. All logs and engine executions will magically appear here.</div>
</div>
<style>
    @keyframes pulseFade {
        0% { transform: scale(0.95); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0px 0px 8px rgba(249,115,22,0.3));}
        100% { transform: scale(0.95); opacity: 0.7; }
    }
</style>
"""
            st.markdown(empty_state_html, unsafe_allow_html=True)
        else:
            html_logs = "<div class='logs-container'>"
            for log in display_logs:
                msg = log['message']
                ts = log['timestamp']
                clean_msg = msg.replace("[EXEC] ", "").replace("[SYS] ", "")
                
                # Dynamic Icon parsing
                icon = "⚙️"
                if "authenticated" in clean_msg.lower() or "provisioned" in clean_msg.lower() or "session" in clean_msg.lower(): icon = "👤"
                elif "enabled" in clean_msg.lower(): icon = "⚡"
                elif "halted" in clean_msg.lower(): icon = "🛑"
                elif "error" in clean_msg.lower() or "failed" in clean_msg.lower(): icon = "⚠️"
                elif "sandbox" in clean_msg.lower(): icon = "🧠"

                styled_text = clean_msg
                if "enabled" in clean_msg.lower(): styled_text = clean_msg.replace("enabled", "<span class='status-pill status-enabled'>ACTIVE</span>")
                elif "halted" in clean_msg.lower(): styled_text = clean_msg.replace("halted", "<span class='status-pill status-halted'>HALTED</span>")
                elif "executed" in clean_msg.lower(): styled_text = clean_msg.replace("executed", "<span class='status-pill status-executed'>EXECUTED</span>")
                
                html_logs += f"""
<div class='log-entry-card' style='display: flex; gap: 12px; align-items: flex-start;'>
    <div style='font-size: 1.2rem; background: rgba(249,115,22,0.1); padding: 5px; border-radius: 8px;'>{icon}</div>
    <div style='flex-grow: 1;'>
        <div class='log-timestamp'>{ts}</div>
        <div class='log-text'>{styled_text}</div>
    </div>
</div>
"""
            html_logs += "</div>"
            st.markdown(html_logs, unsafe_allow_html=True)


    # -------------------------------------------------------------------------
    # AI PLAYGROUND 
    # -------------------------------------------------------------------------
    elif page == "🧠 Inference Engine":
        st.markdown("<h1 class='main-title'>Model Sandbox</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Test standard generations manually in isolation.</p>", unsafe_allow_html=True)
        
        st.markdown("<div style='font-size: 1rem; font-weight: 700; margin-bottom: 12px;'>Direct LLM Interface</div>", unsafe_allow_html=True)
        
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
                    
                    # Debug Info for User - Shows if mock was used or real AI
                    if "[MOCK]" in ai_response or "[System:" in ai_response:
                        st.error(f"Generation Issue Detected: {ai_response}")
                    else:
                        st.markdown("<div style='font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Target Response</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='background: #f8fafc; border: 1px solid #e5e7eb; padding: 20px; border-radius: 12px; font-size: 14px; color: #1e293b; line-height: 1.6;'>{ai_response}</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SETTINGS / INTEGRATIONS 
    # -------------------------------------------------------------------------
    elif page == "⚙️ Integrations":
        st.markdown("<h1 class='main-title'>Settings & Integrations</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Manage credentials and system configurations.</p>", unsafe_allow_html=True)

        # Integration Status Cards - 3 columns
        c1, c2, c3 = st.columns(3)

        integrations = [
            {
                "col": c1, "icon": "🔗", "name": "LinkedIn", "desc": "Graph API v2",
                "detail": "Outreach & lead generation pipeline",
                "active": st.session_state.get("pref_linkedin", True)
            },
            {
                "col": c2, "icon": "📧", "name": "Email Relay", "desc": "AWS SES",
                "detail": "Automated cold email sequences",
                "active": st.session_state.get("pref_email", True)
            },
            {
                "col": c3, "icon": "💬", "name": "WhatsApp", "desc": "Cloud API",
                "detail": "Real-time lead notifications",
                "active": st.session_state.get("pref_whatsapp", True)
            },
        ]

        for item in integrations:
            status_label = "● Live" if item["active"] else "● Offline"
            status_color = "#22C55E" if item["active"] else "#EF4444"
            badge_bg = "#DCFCE7" if item["active"] else "#FEE2E2"
            with item["col"]:
                st.markdown(f"""
                <div class="saas-card" style="text-align:center; padding: 28px 20px;">
                    <div style="font-size:2.2rem; margin-bottom:12px;">{item["icon"]}</div>
                    <div style="font-weight:700; font-size:15px; color:#1F2937; margin-bottom:4px;">{item["name"]}</div>
                    <div style="font-size:12px; color:#6B7280; margin-bottom:14px;">{item["desc"]}</div>
                    <div style="display:inline-block; background:{badge_bg}; color:{status_color}; font-size:12px; font-weight:700; padding:4px 12px; border-radius:99px; margin-bottom:14px;">{status_label}</div>
                    <div style="font-size:12px; color:#9CA3AF;">{item["detail"]}</div>
                </div>
                """, unsafe_allow_html=True)

        # Gemini AI Card (full width)
        st.markdown("""
        <div class="saas-card" style="display:flex; align-items:center; gap:24px; padding:24px 30px;">
            <div style="font-size:2.5rem;">🤖</div>
            <div style="flex:1;">
                <div style="font-weight:700; font-size:15px; color:#1F2937; margin-bottom:4px;">Gemini AI Engine</div>
                <div style="font-size:13px; color:#6B7280;">Model: gemini-2.0-flash &nbsp;|&nbsp; Avg. Response: ~1.2s &nbsp;|&nbsp; Mode: Production</div>
            </div>
            <div style="background:#DCFCE7; color:#166534; font-size:12px; font-weight:700; padding:6px 16px; border-radius:99px;">● Connected</div>
        </div>
        """, unsafe_allow_html=True)

        # Platform toggles to actually control them
        st.markdown("<div style='font-size: 1rem; font-weight: 700; margin-bottom: 12px; margin-top: 24px;'>Enable / Disable Channels</div>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1: st.toggle("LinkedIn Graph API", key="pref_linkedin")
        with t2: st.toggle("SES Email Relay", key="pref_email")
        with t3: st.toggle("WhatsApp Cloud API", key="pref_whatsapp")
