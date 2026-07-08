# 🤖 Personalized Networking Assistant

An AI-powered web application that helps users generate personalized networking conversation starters, verify facts, and manage conversation history using modern NLP models.

---

## 🚀 Features

- 🎯 AI-Based Event Theme Extraction (DistilBERT)
- 💬 Personalized Conversation Starter Generation (GPT-2)
- 📚 Wikipedia Fact Checker
- 📝 Conversation History
- 👍 Feedback Management
- ⚡ FastAPI REST Backend
- 🎨 Streamlit Interactive Frontend
- ✅ Unit Testing with pytest
- 📂 Modular Project Architecture

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | Backend API |
| Streamlit | Frontend UI |
| DistilBERT | Theme Extraction |
| GPT-2 | Conversation Generation |
| Wikipedia API | Fact Checking |
| JSON | Data Storage |
| pytest | Unit Testing |

---

# 📁 Project Structure

```text
Personalized-Networking-Assistant/
│
├── backend/
│   ├── main.py
│   ├── event_analyzer.py
│   ├── topic_generator.py
│   ├── fact_checker.py
│   └── history_logger.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   └── test_backend.py
│
├── history.json
├── feedback.json
├── requirements.txt
├── run.py
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/Personalized-Networking-Assistant.git
```

Navigate to the project

```bash
cd Personalized-Networking-Assistant
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend URL

```
http://127.0.0.1:8000
```

Swagger API

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

---

# 🧪 Run Tests

```bash
pytest
```

---

# 🔄 Application Workflow

1. User opens the Streamlit application.
2. User enters an event description and interests.
3. FastAPI receives the request.
4. DistilBERT extracts important themes.
5. GPT-2 generates networking conversation starters.
6. Wikipedia API verifies facts.
7. History is stored in `history.json`.
8. User feedback is stored in `feedback.json`.
9. Results are displayed on the Streamlit interface.

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /analyze | Analyze event themes |
| POST | /generate | Generate conversation starters |
| GET | /factcheck | Verify facts |
| GET | /history | View conversation history |
| POST | /feedback | Save user feedback |

---

# 📸 Screenshots

### Home Page

> *(Add Screenshot Here)*

### Conversation Generator

> *(Add Screenshot Here)*

### Fact Checker

> *(Add Screenshot Here)*

### History

> *(Add Screenshot Here)*

---

# 📈 Future Enhancements

- User Authentication
- Database Integration (MongoDB/PostgreSQL)
- OpenAI / Gemini Integration
- Multi-language Support
- Cloud Deployment
- Docker Support

---

# 👨‍💻 Author

**Shashank Goud**

B.Tech (Artificial Intelligence)

---

# ⭐ Support

If you found this project useful, please ⭐ star this repository.
