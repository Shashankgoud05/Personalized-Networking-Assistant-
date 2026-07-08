import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.topic_generator import TopicGenerator

class TestTopicGenerator(unittest.TestCase):

    def test_generate_empty_inputs(self):
        """Verifies empty inputs return default icebreaker starter questions without loading models."""
        generator = TopicGenerator()
        result = generator.generate_topics("", [])
        self.assertEqual(len(result), 3)
        self.assertIn("What has been your favorite part", result[2])

    @patch("backend.topic_generator.pipeline")
    def test_generate_topics_success(self, mock_pipeline):
        """Verifies GPT-2 output processing and extraction of unique topics."""
        mock_gen_pipeline = MagicMock()
        # Mock pipeline output returning prompt plus list items
        mock_gen_pipeline.return_value = [{
            "generated_text": "Event: Tech Meetup\nInterests: AI\nGenerate 3 engaging professional networking icebreaker questions:\n1. 1. What are your views on Generative AI trends?\n2. How do you implement Pytest?\n3. What challenges do you face in deployment?"
        }]
        mock_pipeline.return_value = mock_gen_pipeline
        
        generator = TopicGenerator()
        result = generator.generate_topics("Tech Meetup", ["AI"], count=3)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "What are your views on Generative AI trends?")
        self.assertEqual(result[1], "How do you implement Pytest?")

    @patch("backend.topic_generator.pipeline")
    def test_generate_topics_exception_fallback(self, mock_pipeline):
        """Verifies error handling during GPT-2 generation defaults to high-quality fallback questions."""
        mock_gen_pipeline = MagicMock()
        mock_gen_pipeline.side_effect = RuntimeError("OutOfMemoryError on local device")
        mock_pipeline.return_value = mock_gen_pipeline
        
        generator = TopicGenerator()
        result = generator.generate_topics("Hackathon", ["Python"], count=3)
        
        self.assertEqual(len(result), 3)
        self.assertIn("challeng", result[1])  # "What do you think is the biggest challenge..."
        self.assertTrue(any("Python" in r for r in result))

if __name__ == "__main__":
    unittest.main()
