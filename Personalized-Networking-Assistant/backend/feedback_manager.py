import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Locate feedback.json at the project root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDBACK_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "feedback.json"))

class FeedbackManager:
    """
    Manages reading and writing rating feedback and text comments
    to the feedback.json database located at the root of the project.
    """
    def __init__(self, file_path: str = FEEDBACK_PATH):
        self.file_path = file_path
        # Ensure file exists and contains a valid empty JSON array if missing/corrupt
        self._initialize_file()

    def _initialize_file(self):
        """Creates the feedback file with empty array if it doesn't exist or is invalid."""
        if not os.path.exists(self.file_path):
            logger.info(f"Initializing new feedback file at: {self.file_path}")
            self._write_raw([])
            return
            
        # Verify JSON validity
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    logger.warning("Feedback file did not contain a list. Resetting to empty list.")
                    self._write_raw([])
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Feedback file is corrupt or unreadable ({e}). Re-initializing to empty list.")
            self._write_raw([])

    def _write_raw(self, data: List[Dict[str, Any]]):
        """Writes Python lists straight into the feedback file as structured JSON."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to write feedback file at {self.file_path}: {e}")

    def add_feedback(self, rating: int, comment: str) -> Dict[str, Any]:
        """
        Appends a new user rating and text comment.
        
        Args:
            rating (int): A rating score from 1 to 5.
            comment (str): Text review description.
            
        Returns:
            Dict[str, Any]: The newly created and saved feedback record.
        """
        # Validate rating range
        rating = max(1, min(5, rating))
        
        new_record = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "comment": comment.strip()
        }
        
        try:
            # Read existing
            feedbacks = self.get_feedback()
            # Append new record at the beginning (most recent first)
            feedbacks.insert(0, new_record)
            # Write back
            self._write_raw(feedbacks)
            logger.info(f"Successfully saved user feedback with ID {new_record['id']}")
            return new_record
        except Exception as e:
            logger.error(f"Error saving feedback: {str(e)}")
            return new_record

    def get_feedback(self) -> List[Dict[str, Any]]:
        """
        Retrieves all user feedback.
        
        Returns:
            List[Dict[str, Any]]: List of feedback dictionaries.
        """
        self._initialize_file()
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read feedback from {self.file_path}: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculates simple analytics (average rating, count) from feedback logs.
        
        Returns:
            Dict[str, Any]: Statistical overview containing count, average, and breakdown.
        """
        feedbacks = self.get_feedback()
        if not feedbacks:
            return {
                "count": 0,
                "average_rating": 0.0,
                "breakdown": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            }
            
        total = sum(item["rating"] for item in feedbacks)
        count = len(feedbacks)
        avg = round(total / count, 2)
        
        breakdown = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for item in feedbacks:
            r = item["rating"]
            if r in breakdown:
                breakdown[r] += 1
                
        return {
            "count": count,
            "average_rating": avg,
            "breakdown": breakdown
        }

if __name__ == "__main__":
    # Standalone quick test
    mgr = FeedbackManager()
    print("Adding sample feedback...")
    mgr.add_feedback(rating=5, comment="Excellent AI model outputs! Saves me time.")
    mgr.add_feedback(rating=4, comment="Good UI, topics could be slightly more casual.")
    print("\nFeedback Statistics:")
    print(mgr.get_statistics())
