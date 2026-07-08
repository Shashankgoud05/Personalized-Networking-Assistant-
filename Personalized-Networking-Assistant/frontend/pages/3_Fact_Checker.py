import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Fact Checker - Networking Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom styling injection
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
    .fact-card {
        background: rgba(255, 138, 0, 0.05);
        border-left: 5px solid #ff8a00;
        border-radius: 8px;
        padding: 20px;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Wikipedia Fact Checker</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8c9ba5;'>Verify technical terminologies, frameworks, or corporate entities before launching conversations.</p>", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("""
<div class='glass-card'>
    <b>💡 Why verify?</b><br/>
    Stating incorrect or outdated technical facts is a common conversation breaker. Quickly search a framework or language definition to stay confident.
</div>
""", unsafe_allow_html=True)

# Search field UI
query = st.text_input(
    "Search Topic",
    placeholder="E.g., Pytest, FastAPI, DistilBERT, OpenAI",
    help="Type in the term you want to fetch and fact-check."
)

if st.button("🔍 Verify Topic"):
    if not query.strip():
        st.error("❌ Please input a valid topic.")
    else:
        with st.spinner(f"Searching Wikipedia database for '{query}'..."):
            payload = {"topic": query}
            try:
                response = requests.post(f"{BACKEND_URL}/factcheck", json=payload, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    
                    if result["found"]:
                        st.success("✅ Topic found!")
                        st.markdown(f"""
                        <div class='fact-card'>
                            <h3 style='margin-top:0;color:#ff8a00;'>📖 {result['title']}</h3>
                            <p style='color:#e0e6ed;line-height:1.6;'>{result['summary']}</p>
                            <a href='{result['url']}' target='_blank' style='color:#da1b60;text-decoration:none;font-weight:600;'>🔗 View Full Wikipedia Page →</a>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ Topic status: {result['status']}")
                        st.markdown(f"""
                        <div class='glass-card'>
                            {result['summary']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Backend returned error: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: Could not connect to API backend: {e}")
