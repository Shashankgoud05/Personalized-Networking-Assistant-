import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.fact_checker import FactChecker

class TestFactChecker(unittest.TestCase):

    def test_fact_check_empty_input(self):
        """Verifies searching empty topics returns early validation error message."""
        checker = FactChecker()
        result = checker.check_fact("")
        self.assertFalse(result["found"])
        self.assertEqual(result["title"], "")
        self.assertIn("valid topic", result["summary"])

    @patch("wikipediaapi.Wikipedia.page")
    def test_fact_check_success(self, mock_page_method):
        """Verifies successful retrieval of existing Wikipedia article summary and link."""
        mock_page = MagicMock()
        mock_page.exists.return_value = True
        mock_page.title = "FastAPI"
        mock_page.summary = "FastAPI is a modern web framework."
        mock_page.fullurl = "https://en.wikipedia.org/wiki/FastAPI"
        
        mock_page_method.return_value = mock_page
        
        checker = FactChecker()
        result = checker.check_fact("FastAPI")
        
        self.assertTrue(result["found"])
        self.assertEqual(result["title"], "FastAPI")
        self.assertEqual(result["summary"], "FastAPI is a modern web framework.")
        self.assertEqual(result["url"], "https://en.wikipedia.org/wiki/FastAPI")

    @patch("wikipediaapi.Wikipedia.page")
    def test_fact_check_not_found(self, mock_page_method):
        """Verifies searching non-existent items displays appropriate search recommendations."""
        mock_page = MagicMock()
        mock_page.exists.return_value = False
        
        mock_page_method.return_value = mock_page
        
        checker = FactChecker()
        result = checker.check_fact("SDFKLJSDHFLK")
        
        self.assertFalse(result["found"])
        self.assertIn("Could not find an exact Wikipedia match", result["summary"])

    @patch("wikipediaapi.Wikipedia.page")
    def test_fact_check_api_exception(self, mock_page_method):
        """Verifies API connection failures return informative network helper messages."""
        mock_page_method.side_effect = Exception("Wikipedia servers down")
        
        checker = FactChecker()
        result = checker.check_fact("Python")
        
        self.assertFalse(result["found"])
        self.assertIn("Wikipedia query failed", result["summary"])

if __name__ == "__main__":
    unittest.main()
