import streamlit as st
import requests
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="History Logs - Networking Assistant",
    page_icon="📅",
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
    .log-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1.2rem;
    }
    .log-meta {
        font-size: 0.85rem;
        color: #8c9ba5;
        margin-bottom: 10px;
    }
    .log-title {
        color: #ff8a00;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 5px;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 5px;
    }
    .badge-positive { background-color: rgba(0, 200, 83, 0.15); color: #00c853; border: 1px solid #00c853; }
    .badge-formal { background-color: rgba(41, 121, 255, 0.15); color: #2979ff; border: 1px solid #2979ff; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Conversation History Logs</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8c9ba5;'>Browse and search your past AI event queries and icebreaker recommendations.</p>", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

# Main action section: Clear logs
col_action1, col_action2 = st.columns([6, 1])

with col_action2:
    if st.button("🗑️ Clear Logs", help="Permanently delete all logs in history.json"):
        try:
            clear_resp = requests.delete(f"{BACKEND_URL}/history", timeout=5)
            if clear_resp.status_code == 200:
                st.success("History database successfully wiped!")
                st.rerun()
            else:
                st.error("Failed to clear database.")
        except Exception as e:
            st.error(f"Error reaching server: {e}")

# Fetch records
history_list = []
try:
    response = requests.get(f"{BACKEND_URL}/history", timeout=5)
    if response.status_code == 200:
        history_list = response.json()
except Exception as e:
    st.error(f"Could not retrieve history logs: {e}")

if not history_list:
    st.info("📂 No transaction records found. Generate topics to seed the log database!")
else:
    # Search filter field
    search_query = st.text_input("🔍 Search Logs", placeholder="Type event name or interest to filter logs...")
    
    # Render logs
    filtered_count = 0
    for item in history_list:
        # Search criteria matches event description or interests
        interests_str = " ".join(item["interests"])
        if (search_query.lower() in item["event_description"].lower()) or (search_query.lower() in interests_str.lower()):
            filtered_count += 1
            
            # Format timestamp
            dt_obj = datetime.fromisoformat(item["timestamp"])
            formatted_time = dt_obj.strftime("%b %d, %Y @ %I:%M %p")
            
            analysis = item["analysis"]
            sentiment = analysis.get("sentiment_label", "UNKNOWN")
            badge_class = "badge-positive" if sentiment == "POSITIVE" else "badge-formal"
            
            st.markdown(f"""
            <div class='log-item'>
                <div class='log-meta'>
                    <span>📅 {formatted_time}</span> | 
                    <span>🆔 ID: {item['id']}</span>
                </div>
                <div class='log-title'>🏢 Event: {item['event_description']}</div>
                <div style='margin-bottom: 10px;'>
                    <span class='badge {badge_class}'>Tone: {analysis.get('tone', 'Standard')}</span>
                    <span style='color:#8c9ba5; font-size:0.9rem;'>Interests: <b>{', '.join(item['interests'])}</b></span>
                </div>
                <div style='background: rgba(255,255,255,0.01); border-radius: 8px; padding: 12px; border: 1px dashed rgba(255,255,255,0.04);'>
                    <b style='color:#da1b60;'>Generated Icebreakers:</b>
                    <ol style='margin: 8px 0 0 0; padding-left: 20px; color:#b2c0cc; line-height:1.6;'>
                        {"".join(f"<li>\"{topic}\"</li>" for topic in item['generated_topics'])}
                    </ol>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    if filtered_count == 0 and search_query:
        st.warning(f"No records match query search: '{search_query}'")
