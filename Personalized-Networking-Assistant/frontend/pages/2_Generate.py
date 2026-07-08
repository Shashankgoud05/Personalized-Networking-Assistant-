import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Generate Icebreakers - Networking Assistant",
    page_icon="💡",
    layout="wide"
)

# Custom styles injection
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
    .topic-card {
        background: rgba(218, 27, 96, 0.05);
        border-left: 5px solid #da1b60;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        color: #e0e6ed;
    }
    .advice-card-positive {
        background: rgba(0, 200, 83, 0.05);
        border-left: 5px solid #00c853;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 1.5rem;
    }
    .advice-card-formal {
        background: rgba(41, 121, 255, 0.05);
        border-left: 5px solid #2979ff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Generate Conversation Starters</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8c9ba5;'>Enter details about the event and your interests to generate personalized talking points.</p>", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

# Form layout
with st.form("generation_form"):
    st.markdown("### 📋 Event Metadata & Interests")
    
    event_description = st.text_area(
        "Event Description", 
        placeholder="E.g., PyCon 2026 conference focused on Python backend tools and machine learning integration.",
        help="Paste the event flyer, description, invitation email, or write a short summary."
    )
    
    interests_input = st.text_input(
        "Your Professional Interests (comma-separated)",
        placeholder="E.g., Web API, Pytest, LangChain, Kubernetes",
        help="Input topics or tech domains you feel comfortable talking about."
    )
    
    count = st.slider("Number of starters to generate", min_value=1, max_value=5, value=3)
    
    submitted = st.form_submit_button("💡 Generate Icebreakers")

# Triggered actions on form submission
if submitted:
    if not event_description.strip():
        st.error("❌ Please provide an event description.")
    elif not interests_input.strip():
        st.error("❌ Please provide at least one interest.")
    else:
        # Pre-process interests input list
        interests_list = [i.strip() for i in interests_input.split(",") if i.strip()]
        
        # Call Backend
        with st.spinner("🧠 AI models are processing... This may take a few seconds as the model runs locally."):
            payload = {
                "event_description": event_description,
                "interests": interests_list,
                "count": count
            }
            try:
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Starters generated successfully!")
                    
                    # Display Event Tone Analysis
                    analysis = data["analysis"]
                    sentiment = analysis["sentiment_label"]
                    tone = analysis["tone"]
                    advice = analysis["networking_advice"]
                    
                    st.markdown("### 📊 Event Tone Assessment")
                    
                    if sentiment == "POSITIVE":
                        st.markdown(f"""
                        <div class='advice-card-positive'>
                            <b style='color:#00c853;'>Tone: {tone}</b><br/>
                            <p style='margin: 5px 0 0 0; color:#b2c0cc;'>{advice}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='advice-card-formal'>
                            <b style='color:#2979ff;'>Tone: {tone}</b><br/>
                            <p style='margin: 5px 0 0 0; color:#b2c0cc;'>{advice}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display Generated Topics
                    st.markdown("### 💡 Recommended Conversation Starters")
                    for idx, topic in enumerate(data["generated_topics"], 1):
                        st.markdown(f"""
                        <div class='topic-card'>
                            <b>Option #{idx}</b><br/>
                            <span style='font-size:1.15rem; font-style:italic;'>"{topic}"</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                else:
                    st.error(f"❌ Backend error: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: Could not reach the API backend. Verify FastAPI is running. Details: {e}")
