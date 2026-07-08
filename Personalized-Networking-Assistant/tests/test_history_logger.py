import unittest
import os
import json
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.history_logger import HistoryLogger

class TestHistoryLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary file to use as the history store for tests
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close() # Close it so our class can write to it
        self.logger = HistoryLogger(file_path=self.temp_file.name)

    def tearDown(self):
        # Clean up temporary file after each test
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_initialization(self):
        """Verifies new files are correctly initialized as empty JSON list arrays."""
        self.assertTrue(os.path.exists(self.temp_file.name))
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(data, [])

    def test_log_entry(self):
        """Verifies logging entries adds detailed transaction payloads."""
        event_desc = "Web Dev Summit"
        interests = ["FastAPI", "React"]
        analysis = {"sentiment_label": "POSITIVE", "tone": "Welcoming", "networking_advice": "Smile"}
        topics = ["How do you structure FastAPI?"]
        
        entry = self.logger.log_entry(event_desc, interests, analysis, topics)
        
        self.assertIsNotNone(entry["id"])
        self.assertEqual(entry["event_description"], event_desc)
        self.assertEqual(entry["interests"], interests)
        self.assertEqual(entry["generated_topics"], topics)
        
        # Verify read contains the entry
        history = self.logger.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["id"], entry["id"])

    def test_clear_history(self):
        """Verifies clear database command resets content to empty list array."""
        self.logger.log_entry("A", ["B"], {}, ["C"])
        self.assertEqual(len(self.logger.get_history()), 1)
        
        success = self.logger.clear_history()
        self.assertTrue(success)
        self.assertEqual(len(self.logger.get_history()), 0)

if __name__ == "__main__":
    unittest.main()
