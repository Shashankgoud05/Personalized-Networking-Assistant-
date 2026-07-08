import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="AI Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS with Google Fonts (Outfit) and Glassmorphism aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main body background */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #151a24 100%);
        color: #e0e6ed;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0b0d12 !important;
    }
    
    /* Header Gradient styling */
    .main-header {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #ff8a00 0%, #da1b60 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.25rem;
        color: #8c9ba5;
        margin-bottom: 2.5rem;
    }
    
    /* Glassmorphism Card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(218, 27, 96, 0.4);
    }
    
    .card-title {
        color: #ff8a00;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-content {
        color: #b2c0cc;
        line-height: 1.6;
    }
    
    /* Buttons customization */
    .stButton>button {
        background: linear-gradient(90deg, #ff8a00 0%, #da1b60 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(218, 27, 96, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(218, 27, 96, 0.5) !important;
    }
    
    /* Success, Info, Warning Boxes styling override */
    div.stAlert {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #e0e6ed !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Page Layout
st.markdown("<h1 class='main-header'>Personalized Networking Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Elevate your professional networking with the power of Artificial Intelligence.</p>", unsafe_allow_html=True)

# Quick connection health check to backend API
backend_url = "http://127.0.0.1:8000/"
backend_status = False

try:
    response = requests.get(backend_url, timeout=2)
    if response.status_code == 200:
        backend_status = True
except Exception:
    backend_status = False

# Display backend status indicator
if backend_status:
    st.sidebar.success("● Backend Service: Connected")
else:
    st.sidebar.error("○ Backend Service: Disconnected (Start API server)")

# Welcome banner and details
st.markdown(f"""
<div class='glass-card'>
    <div class='card-title'>🤝 Welcome, Future Networker!</div>
    <div class='card-content'>
        Whether you are attending a tech summit, a business seminar, or a local developer meetup, starting conversations can be intimidating. 
        The <b>Personalized Networking Assistant</b> uses state-of-the-art Natural Language Processing to analyze event details and generate highly tailored conversation starters based on your professional interests.
    </div>
</div>
""", unsafe_allow_html=True)

# Features grid using 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='glass-card'>
        <div class='card-title'>📊 Event Analyzer</div>
        <div class='card-content'>
            Powered by <b>DistilBERT</b>, this module reviews the description and tone of the event. It gives you tips on whether to adopt a warm/casual style or prepare for a structured, formal introduction.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='glass-card'>
        <div class='card-title'>💡 Conversation Generator</div>
        <div class='card-content'>
            Uses <b>GPT-2</b> to generate personalized icebreaker questions based on your interests and the event's theme, giving you conversation starters instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='glass-card'>
        <div class='card-title'>🔍 Fact Checker</div>
        <div class='card-content'>
            Integrated with the <b>Wikipedia API</b>, this tool lets you verify facts or search unfamiliar technologies before you initiate conversations, keeping your talking points accurate.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Bottom section: Guide to use
st.markdown("### How to Get Started")
st.info("👈 Use the sidebar navigation menu to browse different modules of the system.")

# Architecture summary
with st.expander("🛠 View Application Architecture & Technologies"):
    st.markdown("""
    This project is built using a modern Full-Stack AI decoupling architecture:
    *   **Frontend**: Built with **Streamlit** for quick, reactive, and visually pleasing user interfaces.
    *   **Backend**: Powered by **FastAPI** providing high-performance, asynchronous REST API endpoints.
    *   **AI Pipelines**: Uses **Hugging Face Transformers** to run offline inferences locally.
        *   *DistilBERT*: Fine-tuned SST-2 model for sentiment classification.
        *   *GPT-2*: Autoregressive language model for creative prompt-based text generation.
    *   **Fact Checking**: Integrates with **Wikipedia API** for external informational lookups.
    *   **Storage**: Lightweight persistent file-based data records (`history.json` and `feedback.json`).
    """)
