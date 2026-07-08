import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Home Dashboard - Networking Assistant",
    page_icon="📊",
    layout="wide"
)

# Reuse custom styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #151a24 100%); color: #e0e6ed; }
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #ff8a00 0%, #da1b60 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem;
    }
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        color: #ff8a00;
        text-shadow: 0 0 10px rgba(255, 138, 0, 0.2);
    }
    .metric-label {
        font-size: 1rem;
        color: #8c9ba5;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>System Dashboard & Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8c9ba5;'>Summary of generated networking ideas and client feedback metrics.</p>", unsafe_allow_html=True)

# Fetch stats from backend
BACKEND_URL = "http://127.0.0.1:8000"
history_count = 0
avg_rating = 0.0
feedback_count = 0

try:
    # Get history
    hist_resp = requests.get(f"{BACKEND_URL}/history", timeout=2)
    if hist_resp.status_code == 200:
        history_count = len(hist_resp.json())
        
    # Get feedback
    fb_resp = requests.get(f"{BACKEND_URL}/feedback", timeout=2)
    if fb_resp.status_code == 200:
        stats = fb_resp.json().get("statistics", {})
        avg_rating = stats.get("average_rating", 0.0)
        feedback_count = stats.get("count", 0)
except Exception:
    st.warning("⚠️ Could not connect to the backend server to pull real-time analytics. Please run the backend first!")

# Display metrics grid
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <div class='metric-value'>{history_count}</div>
        <div class='metric-label'>Scenarios Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <div class='metric-value'>{"★" * int(round(avg_rating)) if avg_rating > 0 else "N/A"} ({avg_rating})</div>
        <div class='metric-label'>Avg User Rating</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='glass-card' style='text-align: center;'>
        <div class='metric-value'>{feedback_count}</div>
        <div class='metric-label'>Feedback Responses</div>
    </div>
    """, unsafe_allow_html=True)

# Quick Networking Cheat Sheet Card
st.markdown("""
<div class='glass-card'>
    <h3 style='color:#ff8a00;margin-top:0;'>💡 Gold Rules of Professional Networking</h3>
    <ul style='color:#b2c0cc;line-height:1.8;padding-left:20px;'>
        <li><b>Listen First</b>: Networking isn't just pitching. Listen 70% of the time, talk 30%.</li>
        <li><b>Have a Hook</b>: Use generated icebreaker questions rather than generic inquiries. Focus on joint interests.</li>
        <li><b>Check the Facts</b>: Never state claims or technological facts you're unsure about. Use our Wikipedia Fact Checker.</li>
        <li><b>Follow Up Early</b>: Connect on LinkedIn or email within 24-48 hours mentioning a specific topic you discussed.</li>
        <li><b>Provide Value</b>: Always ask "How can I help you in your current venture?" rather than just asking for favors.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
