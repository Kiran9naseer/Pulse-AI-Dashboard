# =============================================================================
# automation/ai_reply.py - AI Reply Generation Module (Gemini)
# =============================================================================
# Purpose: Utilizes Google Gemini AI for contextual generation.
#          - Features robust .env loading for API verification.
#          - Gracefully falls back to mock responses if key is missing/invalid.
# =============================================================================

import os
from pathlib import Path
from dotenv import load_dotenv

# --- ROBUST PATH LOADING ---
# Find project root mapping directly regardless of sys path contexts
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

# API Access is handled inside generate_reply for robustness.


# -----------------------------------------------------------------------------
# FALLBACK RESPONSES (MOCK)
# -----------------------------------------------------------------------------
MOCK_REPLIES = {
    "hello":   "Hello! Thanks for reaching out. How can I assist you today?",
    "help":    "Sure, I'd be happy to help! Could you please provide more details?",
    "price":   "Our pricing plans start at $9/month. Would you like to know more?",
    "support": "Our support team is available 24/7. What issue are you facing?",
    "bye":     "Thank you for contacting us. Have a great day!",
    "default": "Thank you for your message! Our team will get back to you shortly.",
}

def _mock_reply(message: str) -> str:
    """Internal router returning a mocked generic response depending on word tags."""
    msg = message.lower()
    for keyword, reply in MOCK_REPLIES.items():
        if keyword in msg:
            return f"[MOCK] {reply}"
    return f"[MOCK] {MOCK_REPLIES['default']}"


# -----------------------------------------------------------------------------
# MAIN GENERATOR FUNCTION
# -----------------------------------------------------------------------------
def generate_reply(message: str) -> str:
    """
    Produces AI-assisted generative messaging.
    """
    if not message or not message.strip():
        return "Please provide a valid text sequence."

    # Robust Environment Loading (Cloud + Local Compatibility)
    import streamlit as st
    api_key = ""
    
    # 1. 🥇 Priority: Check Streamlit Secrets (for Cloud deployment)
    try:
        if "GEMINI_API_KEY" in st.secrets:
            # Handle both string and nested TOML formats
            raw_key = st.secrets["GEMINI_API_KEY"]
            # Strict cleaning: remove whitespace and any accidental wrapping quotes
            api_key = str(raw_key).strip().replace('"', '').replace("'", "")
            print("[AI] Found and cleaned GEMINI_API_KEY from Secrets.")
    except Exception:
        pass

    # 2. 🥈 Fallback: Check .env / Environment Variables (for Local dev)
    if not api_key:
        if ENV_PATH.exists():
            load_dotenv(ENV_PATH)
        else:
            load_dotenv()
        raw_env_key = os.getenv("GEMINI_API_KEY", "")
        # Strict cleaning for environment variables too
        api_key = str(raw_env_key).strip().replace('"', '').replace("'", "")

    # Validate Access Tokens
    if not api_key:
        print("[AI] ERROR: No GEMINI_API_KEY source found. Deflecting to mock.")
        return _mock_reply(message)
    
    print(f"[AI] Initializing Cloud Inference with key prefix: {api_key[:6]}...")

    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        # Expanded priority mapping based on verified working targets
        models_to_try = [
            "gemini-1.5-flash", 
            "gemini-1.5-pro",
            "gemini-pro",
            "models/gemini-1.5-flash",
            "models/gemini-2.5-flash", 
            "models/gemini-2.5-pro",
            "models/gemini-2.0-flash", 
            "models/gemini-2.0-flash-001",
            "models/gemini-pro"
        ]
        
        last_error = None
        for model_name in models_to_try:
            try:
                print(f"[AI] Trying Inference Node: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Optimized SaaS prompt tuning
                prompt = (
                    "You are the professional Pulse.ai assistant. "
                    "Respond as a high-end AI SaaS employee. "
                    "Keep it concise. "
                    f"Customer Message: {message}"
                )
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    print(f"[AI] Success! Response generated via {model_name}")
                    return response.text.strip()
            except Exception as model_err:
                last_error = model_err
                print(f"[AI] Node {model_name} failed: {str(model_err)}")
                continue
        
        # Full Failure Recovery
        print(f"[AI] CRITICAL: All Inference Nodes exhausted. Final error details: {last_error}")
        return f"[System: All Models Exhausted] Error: {str(last_error)}. Mock: {_mock_reply(message)}"

    except Exception as e:
        error_type = type(e).__name__
        if isinstance(e, ModuleNotFoundError):
            return f"[API Dependency Error] {_mock_reply(message)}"
        return f"[System: {error_type}] {_mock_reply(message)}"
