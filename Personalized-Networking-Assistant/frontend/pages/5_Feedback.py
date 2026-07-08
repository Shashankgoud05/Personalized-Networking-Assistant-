import streamlit as st
import requests
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Submit Feedback - Networking Assistant",
    page_icon="⭐",
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
    .review-item {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        margin-bottom: 1rem;
    }
    .stars {
        color: #ff8a00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>User Reviews & Feedback</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#8c9ba5;'>Submit a review, rate your experience, and check other users' suggestions.</p>", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

col_form, col_stats = st.columns([2, 1])

# Left column: submit form
with col_form:
    with st.form("feedback_form"):
        st.markdown("### ✍️ Write a Review")
        
        rating = st.slider("Rating (1 = Poor, 5 = Excellent)", min_value=1, max_value=5, value=5)
        comment = st.text_area("Your Review Comments", placeholder="How can we make this tool better for you?")
        
        submitted = st.form_submit_button("⭐ Submit Review")
        
    if submitted:
        if not comment.strip():
            st.error("❌ Please provide a review comment.")
        else:
            payload = {
                "rating": rating,
                "comment": comment
            }
            try:
                response = requests.post(f"{BACKEND_URL}/feedback", json=payload, timeout=5)
                if response.status_code == 201:
                    st.success("✅ Thank you for your feedback!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to submit: {response.text}")
            except Exception as e:
                st.error(f"❌ Connection error: Could not reach backend server: {e}")

# Fetch statistics and review list
feedback_list = []
stats = {"count": 0, "average_rating": 0.0, "breakdown": {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}}

try:
    response = requests.get(f"{BACKEND_URL}/feedback", timeout=5)
    if response.status_code == 200:
        data = response.json()
        feedback_list = data.get("feedback_list", [])
        stats = data.get("statistics", {})
except Exception as e:
    st.error(f"Could not load feedback stats: {e}")

# Right column: show aggregate stats
with col_stats:
    st.markdown("### 📊 Rating Overview")
    st.markdown(f"""
    <div class='glass-card' style='text-align:center;'>
        <span style='font-size:3rem; font-weight:800; color:#ff8a00;'>{stats.get('average_rating', 0.0)} / 5.0</span><br/>
        <span style='color:#8c9ba5;'>Average Score ({stats.get('count', 0)} reviews)</span>
    </div>
    """, unsafe_allow_html=True)

# Bottom section: show recent reviews
st.markdown("### 💬 Recent Reviews")
if not feedback_list:
    st.info("No reviews submitted yet. Be the first to leave feedback!")
else:
    for item in feedback_list[:10]:  # Show latest 10 reviews
        dt_obj = datetime.fromisoformat(item["timestamp"])
        formatted_time = dt_obj.strftime("%b %d, %Y")
        
        star_str = "★" * item["rating"] + "☆" * (5 - item["rating"])
        st.markdown(f"""
        <div class='review-item'>
            <div style='display:flex; justify-content:space-between; margin-bottom:5px;'>
                <span class='stars'>{star_str}</span>
                <span style='color:#8c9ba5; font-size:0.85rem;'>📅 {formatted_time}</span>
            </div>
            <p style='margin:0; color:#b2c0cc; font-style:italic;'>"{item['comment']}"</p>
        </div>
        """, unsafe_allow_html=True)
