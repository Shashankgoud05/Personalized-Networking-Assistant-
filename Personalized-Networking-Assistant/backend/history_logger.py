import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Locate history.json at the project root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "history.json"))

class HistoryLogger:
    """
    Manages reading and writing search logs, sentiment outputs, and generated topics
    to the history.json database located at the root of the project.
    """
    def __init__(self, file_path: str = HISTORY_PATH):
        self.file_path = file_path
        # Ensure file exists and contains a valid empty JSON array if missing/corrupt
        self._initialize_file()

    def _initialize_file(self):
        """Creates the history file with empty array if it doesn't exist or is invalid."""
        if not os.path.exists(self.file_path):
            logger.info(f"Initializing new history file at: {self.file_path}")
            self._write_raw([])
            return
            
        # Verify JSON validity
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    logger.warning("History file did not contain a list. Resetting to empty list.")
                    self._write_raw([])
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"History file is corrupt or unreadable ({e}). Re-initializing to empty list.")
            self._write_raw([])

    def _write_raw(self, data: List[Dict[str, Any]]):
        """Writes Python lists straight into the history file as structured JSON."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to write history file at {self.file_path}: {e}")

    def log_entry(self, event_description: str, interests: List[str], analysis: Dict[str, Any], topics: List[str]) -> Dict[str, Any]:
        """
        Creates and appends a new event analysis and generation log record.
        
        Args:
            event_description (str): Text description of event.
            interests (List[str]): User interests.
            analysis (Dict[str, Any]): Sentiment analysis outcome dictionary.
            topics (List[str]): Generated icebreaker topics.
            
        Returns:
            Dict[str, Any]: The newly created and saved history record.
        """
        new_record = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "timestamp": datetime.now().isoformat(),
            "event_description": event_description,
            "interests": interests,
            "analysis": analysis,
            "generated_topics": topics
        }
        
        try:
            # Read existing
            history = self.get_history()
            # Append new record at the beginning (most recent first)
            history.insert(0, new_record)
            # Write back
            self._write_raw(history)
            logger.info(f"Successfully logged new history entry with ID {new_record['id']}")
            return new_record
        except Exception as e:
            logger.error(f"Error logging history: {str(e)}")
            return new_record

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Retrieves all logged history.
        
        Returns:
            List[Dict[str, Any]]: List of history dictionaries.
        """
        self._initialize_file()
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read history from {self.file_path}: {e}")
            return []

    def clear_history(self) -> bool:
        """
        Resets history database to an empty list.
        
        Returns:
            bool: True if clear was successful, False otherwise.
        """
        try:
            self._write_raw([])
            logger.info("History database cleared.")
            return True
        except Exception as e:
            logger.error(f"Failed to clear history: {e}")
            return False

if __name__ == "__main__":
    # Standalone quick test
    logger_test = HistoryLogger()
    print("Writing a mock entry...")
    logger_test.log_entry(
        event_description="Networking Summit",
        interests=["AI", "Startups"],
        analysis={"sentiment_label": "POSITIVE", "tone": "Welcoming", "networking_advice": "Smile!"},
        topics=["How is AI impacting your startup?", "What tech are you building?"]
    )
    print("\nReading history:")
    print(logger_test.get_history()[:1])
