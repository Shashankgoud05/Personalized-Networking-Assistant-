import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, conint

# Import our backend components
from backend.event_analyzer import EventAnalyzer
from backend.topic_generator import TopicGenerator
from backend.fact_checker import FactChecker
from backend.history_logger import HistoryLogger
from backend.feedback_manager import FeedbackManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
analyzer = EventAnalyzer()
generator = TopicGenerator()
checker = FactChecker()
history_logger = HistoryLogger()
feedback_manager = FeedbackManager()

app = FastAPI(
    title="Personalized Networking Assistant API",
    description="Backend API powering event analysis, conversation topic generation, and Wikipedia fact checking.",
    version="1.0.0"
)

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend clients to talk to the backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Pydantic Request/Response Models ----------------

class AnalyzeRequest(BaseModel):
    event_description: str = Field(..., description="Details and context of the networking event.")

class AnalyzeResponse(BaseModel):
    sentiment_label: str
    confidence_score: float
    tone: str
    networking_advice: str

class GenerateRequest(BaseModel):
    event_description: str = Field(..., description="Details and context of the networking event.")
    interests: List[str] = Field(..., description="Topics, tech stacks, or domains you are interested in.")
    count: conint(ge=1, le=5) = Field(3, description="Number of conversation starters to generate.")

class GenerateResponse(BaseModel):
    id: str
    timestamp: str
    event_description: str
    interests: List[str]
    analysis: AnalyzeResponse
    generated_topics: List[str]

class FactCheckRequest(BaseModel):
    topic: str = Field(..., description="Term, technology, or person to query on Wikipedia.")

class FactCheckResponse(BaseModel):
    found: bool
    title: str
    summary: str
    url: str
    status: str

class FeedbackRequest(BaseModel):
    rating: conint(ge=1, le=5) = Field(..., description="User review score between 1 and 5.")
    comment: str = Field("", description="Review description or suggestions.")

class FeedbackResponse(BaseModel):
    success: bool
    record: Dict[str, Any]

class StatisticsResponse(BaseModel):
    count: int
    average_rating: float
    breakdown: Dict[int, int]

class FeedbackListResponse(BaseModel):
    feedback_list: List[Dict[str, Any]]
    statistics: StatisticsResponse

class SuccessResponse(BaseModel):
    success: bool
    message: str

# ---------------- API Routes ----------------

@app.get("/", tags=["General"])
async def root():
    """Welcome endpoint verifying backend health status."""
    return {
        "status": "online",
        "service": "Personalized Networking Assistant API",
        "endpoints": ["/analyze", "/generate", "/factcheck", "/history", "/feedback"]
    }

@app.post("/analyze", response_model=AnalyzeResponse, tags=["AI Core"])
async def analyze_event(req: AnalyzeRequest):
    """
    Analyzes an event description to determine its formal/enthusiastic sentiment tone
    using a Hugging Face DistilBERT model.
    """
    logger.info("Received request for event sentiment analysis.")
    try:
        result = analyzer.analyze(req.event_description)
        return result
    except Exception as e:
        logger.error(f"Error in /analyze endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing sentiment analysis: {str(e)}"
        )

@app.post("/generate", response_model=GenerateResponse, tags=["AI Core"])
async def generate_conversation_topics(req: GenerateRequest):
    """
    Analyzes event context, generates personalized topic starters using GPT-2,
    combines results, logs the transaction to history.json, and returns details.
    """
    logger.info("Received request to generate conversation starters.")
    try:
        # Step 1: Analyze the event
        analysis_result = analyzer.analyze(req.event_description)
        
        # Step 2: Generate conversation icebreakers
        topics = generator.generate_topics(
            event_description=req.event_description,
            interests=req.interests,
            count=req.count
        )
        
        # Step 3: Log the transaction into history
        logged_entry = history_logger.log_entry(
            event_description=req.event_description,
            interests=req.interests,
            analysis=analysis_result,
            topics=topics
        )
        
        return logged_entry
    except Exception as e:
        logger.error(f"Error in /generate endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating icebreaker topics: {str(e)}"
        )

@app.post("/factcheck", response_model=FactCheckResponse, tags=["Utilities"])
async def fact_check_topic(req: FactCheckRequest):
    """
    Queries Wikipedia to verify facts and return page summaries for specific search queries.
    """
    logger.info(f"Received request to check fact: {req.topic}")
    try:
        result = checker.check_fact(req.topic)
        return result
    except Exception as e:
        logger.error(f"Error in /factcheck endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching Wikipedia page: {str(e)}"
        )

@app.get("/history", response_model=List[GenerateResponse], tags=["Database"])
async def get_history_logs():
    """
    Retrieves all past event analyses and generated conversations.
    """
    logger.info("Retrieving history list.")
    try:
        return history_logger.get_history()
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        return []

@app.delete("/history", response_model=SuccessResponse, tags=["Database"])
async def clear_history_logs():
    """
    Clears all items in the history.json database.
    """
    logger.info("Clearing history logs.")
    success = history_logger.clear_history()
    if success:
        return {"success": True, "message": "History logs successfully cleared."}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear history log database."
        )

@app.get("/feedback", response_model=FeedbackListResponse, tags=["Feedback"])
async def get_all_feedback():
    """
    Retrieves feedback submissions and provides rating summary metrics.
    """
    logger.info("Retrieving all user feedback.")
    try:
        records = feedback_manager.get_feedback()
        stats = feedback_manager.get_statistics()
        return {
            "feedback_list": records,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Error retrieving feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch feedback logs: {str(e)}"
        )

@app.post("/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED, tags=["Feedback"])
async def submit_feedback(req: FeedbackRequest):
    """
    Submits user feedback consisting of a rating scale (1-5) and comment details.
    """
    logger.info(f"Submitting feedback rating: {req.rating}")
    try:
        saved_record = feedback_manager.add_feedback(
            rating=req.rating,
            comment=req.comment
        )
        return {
            "success": True,
            "record": saved_record
        }
    except Exception as e:
        logger.error(f"Error adding feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save feedback: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Standalone running of backend server
    print("Starting FastAPI Backend Server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
