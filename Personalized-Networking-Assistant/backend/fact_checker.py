import logging
from typing import Dict, Any
import wikipediaapi

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FactChecker:
    """
    Interfaces with the Wikipedia API to fetch concise summaries and official source links
    for general topics, technologies, or organizations. Helps networkers double-check facts.
    """
    def __init__(self):
        # Wikipedia requires a descriptive User-Agent header to avoid blocking/rate-limiting
        self.user_agent = "PersonalizedNetworkingAssistant/1.0 (shash.gemini@example.com)"
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=self.user_agent,
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

    def check_fact(self, topic: str) -> Dict[str, Any]:
        """
        Queries Wikipedia for a summary and page link of the given topic.
        
        Args:
            topic (str): The term or concept to search for.
            
        Returns:
            Dict[str, Any]: A dictionary containing the summary, page URL, and verification status.
        """
        if not topic.strip():
            return {
                "found": False,
                "title": "",
                "summary": "Please provide a valid topic to fact check.",
                "url": "",
                "status": "No topic provided"
            }

        logger.info(f"Querying Wikipedia for topic: {topic}")
        try:
            page = self.wiki.page(topic)
            
            if page.exists():
                # Truncate summary to first 3 sentences or roughly 300 characters
                summary = page.summary
                if len(summary) > 400:
                    # Try to cut at a sentence boundary
                    end_idx = summary.find('.', 300)
                    if end_idx != -1:
                        summary = summary[:end_idx + 1]
                    else:
                        summary = summary[:400] + "..."
                        
                return {
                    "found": True,
                    "title": page.title,
                    "summary": summary,
                    "url": page.fullurl,
                    "status": "Fact found and verified on Wikipedia."
                }
            else:
                logger.warning(f"Wikipedia page not found for: {topic}")
                # Try capitalization check (sometimes search queries benefit from title casing)
                title_cased = topic.title()
                if title_cased != topic:
                    logger.info(f"Retrying Wikipedia search with title casing: {title_cased}")
                    page_retry = self.wiki.page(title_cased)
                    if page_retry.exists():
                        summary = page_retry.summary
                        if len(summary) > 400:
                            end_idx = summary.find('.', 300)
                            if end_idx != -1:
                                summary = summary[:end_idx + 1]
                            else:
                                summary = summary[:400] + "..."
                        return {
                            "found": True,
                            "title": page_retry.title,
                            "summary": summary,
                            "url": page_retry.fullurl,
                            "status": "Fact found and verified on Wikipedia (casing adjusted)."
                        }

                return {
                    "found": False,
                    "title": topic,
                    "summary": f"Could not find an exact Wikipedia match for '{topic}'. Try checking spelling or using a broader term.",
                    "url": "",
                    "status": "Not found"
                }
                
        except Exception as e:
            logger.error(f"Error querying Wikipedia API: {str(e)}")
            return {
                "found": False,
                "title": topic,
                "summary": f"Wikipedia query failed. Please check your internet connection. Detail: {str(e)}",
                "url": "",
                "status": f"API Error: {str(e)}"
            }

if __name__ == "__main__":
    # Quick standalone test
    checker = FactChecker()
    print("Testing existing page (Python programming language):")
    print(checker.check_fact("Python (programming language)"))
    
    print("\nTesting non-existing page (SDFKLJSDHFLK):")
    print(checker.check_fact("SDFKLJSDHFLK"))
