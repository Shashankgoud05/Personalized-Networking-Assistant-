import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

# We configure absolute import adjustments if running tests directly
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app

client = TestClient(app)

class TestBackendEndpoints(unittest.TestCase):
    
    def test_root_endpoint(self):
        """Verifies the health check root endpoint returns correct status."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")
        
    @patch("backend.main.analyzer.analyze")
    def test_analyze_endpoint(self, mock_analyze):
        """Verifies event text sentiment analysis endpoint works."""
        mock_analyze.return_value = {
            "sentiment_label": "POSITIVE",
            "confidence_score": 0.99,
            "tone": "Welcoming & Enthusiastic",
            "networking_advice": "Great opportunity!"
        }
        
        payload = {"event_description": "Exciting AI Hackathon"}
        response = client.post("/analyze", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sentiment_label"], "POSITIVE")
        self.assertEqual(data["tone"], "Welcoming & Enthusiastic")
        mock_analyze.assert_called_once_with("Exciting AI Hackathon")

    @patch("backend.main.generator.generate_topics")
    @patch("backend.main.analyzer.analyze")
    def test_generate_endpoint(self, mock_analyze, mock_generate):
        """Verifies conversation starter generation endpoint works and logs to history."""
        mock_analyze.return_value = {
            "sentiment_label": "POSITIVE",
            "confidence_score": 0.99,
            "tone": "Welcoming",
            "networking_advice": "Advice text"
        }
        mock_generate.return_value = ["Topic 1", "Topic 2"]
        
        # We patch history_logger to avoid polluting our actual history.json during testing
        with patch("backend.main.history_logger.log_entry") as mock_log:
            mock_log.return_value = {
                "id": "12345",
                "timestamp": "2026-07-08T19:51:25",
                "event_description": "Tech conference",
                "interests": ["Robotics"],
                "analysis": {
                    "sentiment_label": "POSITIVE",
                    "confidence_score": 0.99,
                    "tone": "Welcoming",
                    "networking_advice": "Advice text"
                },
                "generated_topics": ["Topic 1", "Topic 2"]
            }
            
            payload = {
                "event_description": "Tech conference",
                "interests": ["Robotics"],
                "count": 2
            }
            response = client.post("/generate", json=payload)
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["id"], "12345")
            self.assertEqual(len(data["generated_topics"]), 2)
            mock_log.assert_called_once()

    @patch("backend.main.checker.check_fact")
    def test_factcheck_endpoint(self, mock_check):
        """Verifies Wikipedia lookup factcheck endpoint works."""
        mock_check.return_value = {
            "found": True,
            "title": "FastAPI",
            "summary": "FastAPI is a modern web framework.",
            "url": "https://wikipedia.org/wiki/FastAPI",
            "status": "Fact verified."
        }
        
        payload = {"topic": "FastAPI"}
        response = client.post("/factcheck", json=payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["found"])
        self.assertEqual(data["title"], "FastAPI")

    def test_feedback_endpoints(self):
        """Verifies posting and retrieving feedback works against backend database handlers."""
        # Clean test by patching database write actions
        with patch("backend.main.feedback_manager.add_feedback") as mock_add, \
             patch("backend.main.feedback_manager.get_feedback") as mock_get, \
             patch("backend.main.feedback_manager.get_statistics") as mock_stats:
                 
            mock_add.return_value = {"id": "1", "rating": 5, "comment": "Nice!"}
            mock_get.return_value = [{"id": "1", "rating": 5, "comment": "Nice!"}]
            mock_stats.return_value = {"count": 1, "average_rating": 5.0, "breakdown": {5: 1}}
            
            # Test POST /feedback
            post_payload = {"rating": 5, "comment": "Nice!"}
            post_resp = client.post("/feedback", json=post_payload)
            self.assertEqual(post_resp.status_code, 201)
            self.assertTrue(post_resp.json()["success"])
            
            # Test GET /feedback
            get_resp = client.get("/feedback")
            self.assertEqual(get_resp.status_code, 200)
            self.assertEqual(len(get_resp.json()["feedback_list"]), 1)
            self.assertEqual(get_resp.json()["statistics"]["average_rating"], 5.0)

if __name__ == "__main__":
    unittest.main()
