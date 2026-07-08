import os
import logging
from typing import Dict, Any
from transformers import pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine cache directory inside the local project
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "models"))
os.makedirs(CACHE_DIR, exist_ok=True)

class EventAnalyzer:
    """
    Uses a pretrained Hugging Face DistilBERT model to classify the sentiment/tone
    of event descriptions, helping users understand the mood of the networking event.
    """
    def __init__(self):
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.classifier = None

    def load_model(self):
        """Lazy load the model to speed up application startup."""
        if self.classifier is None:
            logger.info(f"Loading sentiment analysis model '{self.model_name}' (cache: {CACHE_DIR})...")
            try:
                self.classifier = pipeline(
                    "sentiment-analysis",
                    model=self.model_name,
                    cache_dir=CACHE_DIR
                )
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                raise RuntimeError(f"Error loading DistilBERT model: {e}")

    def analyze(self, event_description: str) -> Dict[str, Any]:
        """
        Analyzes the sentiment of the provided event description.
        
        Args:
            event_description (str): Text describing the event.
            
        Returns:
            Dict[str, Any]: A dictionary containing the label (e.g. POSITIVE/NEGATIVE),
                            confidence score, and a brief description.
        """
        if not event_description.strip():
            return {
                "label": "NEUTRAL",
                "score": 1.0,
                "message": "Empty event description. Defaulted to neutral sentiment."
            }
            
        self.load_model()
        
        try:
            # Perform inference
            result = self.classifier(event_description)[0]
            label = result["label"]
            score = float(result["score"])
            
            # Map sentiment labels to networking tone interpretations
            if label == "POSITIVE":
                tone = "Welcoming & Enthusiastic"
                advice = "The event description has an encouraging and open tone. Great opportunity for warm conversations!"
            else:
                tone = "Formal & Serious"
                advice = "The event description appears highly structured, formal, or intensive. Focus on professional credentials, industry updates, and concise introductions."
                
            return {
                "sentiment_label": label,
                "confidence_score": score,
                "tone": tone,
                "networking_advice": advice
            }
        except Exception as e:
            logger.error(f"Inference error during analysis: {str(e)}")
            return {
                "sentiment_label": "UNKNOWN",
                "confidence_score": 0.0,
                "tone": "Indeterminate",
                "networking_advice": f"Could not analyze event tone due to model execution failure: {str(e)}"
            }

if __name__ == "__main__":
    # Quick standalone test
    analyzer = EventAnalyzer()
    test_text = "Join us for an exciting technology hackathon filled with learning, coding, and networking with experts!"
    print("Testing positive sentiment event analysis:")
    print(analyzer.analyze(test_text))
    
    test_text_formal = "Corporate alignment meeting on security audits and compliance frameworks. Presence is mandatory."
    print("\nTesting negative/formal sentiment event analysis:")
    print(analyzer.analyze(test_text_formal))
