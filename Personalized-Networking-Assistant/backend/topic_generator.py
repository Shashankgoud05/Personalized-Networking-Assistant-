import os
import logging
import re
from typing import List
from transformers import pipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine cache directory inside the local project
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "models"))
os.makedirs(CACHE_DIR, exist_ok=True)

class TopicGenerator:
    """
    Uses a pretrained Hugging Face GPT-2 model to generate tailored networking icebreakers
    and conversation topics matching a user's interests and the event description.
    """
    def __init__(self):
        self.model_name = "gpt2"
        self.generator = None

    def load_model(self):
        """Lazy load the model to speed up application startup."""
        if self.generator is None:
            logger.info(f"Loading text generation model '{self.model_name}' (cache: {CACHE_DIR})...")
            try:
                # Initialize pipeline for text-generation
                self.generator = pipeline(
                    "text-generation",
                    model=self.model_name,
                    cache_dir=CACHE_DIR
                )
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                raise RuntimeError(f"Error loading GPT-2 model: {e}")

    def generate_topics(self, event_description: str, interests: List[str], count: int = 3) -> List[str]:
        """
        Generates conversation starters based on event context and user interests.
        
        Args:
            event_description (str): Detail about the event.
            interests (List[str]): List of the user's interests or professional topics.
            count (int): Desired number of conversation starters.
            
        Returns:
            List[str]: List of suggested icebreakers/topics.
        """
        if not event_description.strip() or not interests:
            return [
                "Hello! What brings you to this event today?",
                "Hi, I noticed the event has a great turnout. Are you local to this area?",
                "What has been your favorite part of the event so far?"
            ]

        self.load_model()
        interests_str = ", ".join(interests)
        
        # We craft a structured prompt for GPT-2 to perform few-shot or structured generation
        prompt = (
            f"Event: {event_description}\n"
            f"Interests: {interests_str}\n"
            f"Generate {count} engaging professional networking icebreaker questions:\n"
            "1. "
        )
        
        logger.info(f"Generating topics with prompt: {prompt!r}")
        
        try:
            # We set max_new_tokens to prevent long runtime, and clean_up_tokenization_spaces to clean output.
            # Using temperature and top_k or top_p to encourage readable text.
            outputs = self.generator(
                prompt,
                max_new_tokens=80,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.9,
                pad_token_id=50256, # GPT-2 uses 50256 for EOS/PAD
                do_sample=True
            )
            
            generated_text = outputs[0]["generated_text"]
            logger.info(f"Raw generated text: {generated_text}")
            
            # Post-process the output to extract icebreakers
            # We slice off the prompt to inspect only the new tokens
            new_text = generated_text[len(prompt):]
            
            # Add "1. " back to the generated content for parsing if needed
            full_answer = "1. " + new_text
            
            # Find lines matching numbered lists: "1. [text]", "2. [text]", "3. [text]", etc.
            lines = re.split(r'\n|\b\d+\.\s+', full_answer)
            
            topics = []
            for line in lines:
                cleaned = line.strip()
                # Clean up formatting, trailing prompts, or unfinished sentences
                if len(cleaned) > 10 and not cleaned.startswith("Event:") and not cleaned.startswith("Interests:"):
                    # Remove ending punctuation fragments if the model cut off mid-sentence
                    if cleaned[-1] not in ".!?":
                        # Attempt to find the last complete sentence
                        last_period = max(cleaned.rfind('.'), cleaned.rfind('?'), cleaned.rfind('!'))
                        if last_period != -1:
                            cleaned = cleaned[:last_period+1]
                    topics.append(cleaned)
                    
            # Filter unique entries
            unique_topics = []
            for t in topics:
                if t not in unique_topics:
                    unique_topics.append(t)
                    
            # Fallback if generation didn't yield enough clean items
            while len(unique_topics) < count:
                fallback_topics = [
                    f"How do you see the future of {interests[0] if len(interests) > 0 else 'technology'} evolving at events like this?",
                    f"What projects are you working on that relate to {interests[-1] if len(interests) > 0 else 'this field'}?",
                    f"Have you heard about any interesting breakthroughs in {interests[0] if len(interests) > 0 else 'this space'} lately?",
                    f"What's your take on the current developments in our industry?"
                ]
                for ft in fallback_topics:
                    if ft not in unique_topics:
                        unique_topics.append(ft)
                        break
                        
            return unique_topics[:count]
            
        except Exception as e:
            logger.error(f"Text generation error: {str(e)}")
            # Fail-safe static topics based on user inputs
            interest = interests[0] if interests else "industry trends"
            return [
                f"Hi! Are you currently working on anything related to {interest}?",
                f"What do you think is the biggest challenge facing the {interest} field today?",
                f"I'd love to hear your thoughts on how {interest} ties into this event's theme."
            ]

if __name__ == "__main__":
    # Quick standalone test
    generator = TopicGenerator()
    event = "FinTech Summit 2026 for digital banking advancements"
    user_interests = ["Blockchain", "AI Risk Management"]
    print("Testing topic generation:")
    results = generator.generate_topics(event, user_interests, count=3)
    for idx, topic in enumerate(results, 1):
        print(f"{idx}. {topic}")
