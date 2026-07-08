import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.event_analyzer import EventAnalyzer

class TestEventAnalyzer(unittest.TestCase):

    def test_analyze_empty_input(self):
        """Verifies empty strings return a neutral default assessment without running models."""
        analyzer = EventAnalyzer()
        result = analyzer.analyze("   ")
        self.assertEqual(result["label"], "NEUTRAL")
        self.assertEqual(result["score"], 1.0)
        self.assertIn("Empty event description", result["message"])

    @patch("backend.event_analyzer.pipeline")
    def test_analyze_positive_tone(self, mock_pipeline):
        """Verifies POSITIVE sentiment labels map to welcoming tone advices."""
        # Setup mock pipeline output
        mock_classifier = MagicMock()
        mock_classifier.return_value = [{"label": "POSITIVE", "score": 0.98}]
        mock_pipeline.return_value = mock_classifier
        
        analyzer = EventAnalyzer()
        result = analyzer.analyze("A very fun developer festival!")
        
        self.assertEqual(result["sentiment_label"], "POSITIVE")
        self.assertEqual(result["tone"], "Welcoming & Enthusiastic")
        self.assertIn("warm conversations", result["networking_advice"])

    @patch("backend.event_analyzer.pipeline")
    def test_analyze_negative_or_formal_tone(self, mock_pipeline):
        """Verifies NEGATIVE sentiment labels map to formal/compliance advice tags."""
        mock_classifier = MagicMock()
        mock_classifier.return_value = [{"label": "NEGATIVE", "score": 0.85}]
        mock_pipeline.return_value = mock_classifier
        
        analyzer = EventAnalyzer()
        result = analyzer.analyze("Strict security policy briefing.")
        
        self.assertEqual(result["sentiment_label"], "NEGATIVE")
        self.assertEqual(result["tone"], "Formal & Serious")
        self.assertIn("credentials", result["networking_advice"])

    @patch("backend.event_analyzer.pipeline")
    def test_analyze_exception_handling(self, mock_pipeline):
        """Verifies errors during pipeline classification return safe fallback outputs."""
        mock_classifier = MagicMock()
        mock_classifier.side_effect = Exception("GPU out of memory")
        mock_pipeline.return_value = mock_classifier
        
        analyzer = EventAnalyzer()
        result = analyzer.analyze("Some text here")
        
        self.assertEqual(result["sentiment_label"], "UNKNOWN")
        self.assertEqual(result["tone"], "Indeterminate")
        self.assertIn("Could not analyze event tone", result["networking_advice"])

if __name__ == "__main__":
    unittest.main()
