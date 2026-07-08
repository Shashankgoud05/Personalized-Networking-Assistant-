# Personalized Networking Assistant

A production-quality full-stack AI assistant to help developers, entrepreneurs, and event attendees analyze networking event tones, generate personalized conversation starter topics, and verify facts in real-time.

Built using **FastAPI**, **Streamlit**, **Hugging Face Transformers (DistilBERT & GPT-2)**, and the **Wikipedia API**.

---

## Architecture & System Workflows

```text
User Input (Streamlit)
    │
    ▼
FastAPI Server (/generate endpoint)
    │
    ├─► Event Analyzer (DistilBERT sentiment analysis of context)
    ├─► Topic Generator (GPT-2 generating conversation topics)
    │
    ▼
Fact Checker (Wikipedia API verification of topics)
    │
    ▼
History Logger (Writes log record to history.json)
    │
    ▼
JSON response returned to Streamlit
    │
    ▼
Results rendered to the User in Streamlit page UI
```

1.  **Streamlit UI Client**: The user navigates to the Streamlit app (`http://localhost:8501`) and inputs an event details description and their own professional interests.
2.  **FastAPI Server Endpoint**: Streamlit sends a POST request to FastAPI (`http://localhost:8000/generate`).
3.  **Local AI Model Pipeline**:
    *   **DistilBERT** classifies the mood/tone (Welcoming/Formal).
    *   **GPT-2** generates creative conversation icebreaker questions customized for the interests in that context.
    *   *Note: Models cache locally in the `models/` directory inside the project workspace.*
4.  **External Information Integration**: User verifies frameworks or terminologies using the Wikipedia API wrapper.
5.  **Local State Engine**: Interaction logs are recorded into `history.json` and client reviews go into `feedback.json`.

---

## Directory Structure

```text
Personalized-Networking-Assistant/
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── history.json
├── feedback.json
├── backend/
│   ├── event_analyzer.py
│   ├── fact_checker.py
│   ├── feedback_manager.py
│   ├── history_logger.py
│   ├── main.py
│   └── topic_generator.py
├── frontend/
│   ├── app.py
│   └── pages/
│       ├── 1_Home.py
│       ├── 2_Generate.py
│       ├── 3_Fact_Checker.py
│       ├── 4_History.py
│       └── 5_Feedback.py
└── tests/
    ├── test_backend.py
    ├── test_event_analyzer.py
    ├── test_fact_checker.py
    ├── test_history_logger.py
    └── test_topic_generator.py
```

---

## Installation & Setup

### 1. Prerequisites
Make sure Python 3.8+ is installed on your system.

### 2. Create Virtual Environment
Create a virtual environment to manage dependencies isolated from your system packages:
```bash
python -m venv .venv
```
Activate it:
*   **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
*   **Windows (CMD)**: `.venv\Scripts\activate.bat`
*   **Linux/macOS**: `source .venv/bin/activate`

### 3. Install Dependencies
Run:
```bash
pip install -r requirements.txt
```

---

## Running the Application

To run the entire system (FastAPI backend + Streamlit frontend) concurrently, use the launcher orchestrator script:
```bash
python run.py
```
*   **FastAPI backend API**: running on [http://127.0.0.1:8000](http://127.0.0.1:8000)
*   **Streamlit Web application**: running on [http://127.0.0.1:8501](http://127.0.0.1:8501) (open this link in your browser)

---

## API Endpoints List

*   `GET /` - Health check status dashboard.
*   `POST /analyze` - Analyzes event descriptions sentiment using DistilBERT.
*   `POST /generate` - Generates conversation prompts using GPT-2 and logs to history.
*   `POST /factcheck` - Queries Wikipedia for facts verification.
*   `GET /history` - Fetches generated history list.
*   `DELETE /history` - Wipes history logs.
*   `GET /feedback` - Fetches rating scores and comments list.
*   `POST /feedback` - Appends client feedback rating and comment.

---

## Running Automated Tests

Run unit and integration tests using pytest:
```bash
pytest tests/
```
The test suite utilizes mocks for Hugging Face model loaders to verify calculations and API behaviors instantaneously.
