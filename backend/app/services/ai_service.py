import json
import logging
import asyncio
import re
from app.config import config
# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
# pyrefly: ignore [missing-import]
from google.genai import errors
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class AIService:
    _client = genai.Client(api_key=config.GEMINI_API_KEY) if config.GEMINI_API_KEY else None

    @classmethod
    async def _generate(cls, prompt: str, temperature: float = 0.2, retries: int = 2, timeout: float = 10.0) -> str:
        """Helper to generate content asynchronously with retries and backoff."""
        if not cls._client:
            raise HTTPException(status_code=503, detail="AI Service is currently disabled because the GEMINI_API_KEY is not set.")
            
        for attempt in range(retries):
            try:
                def sync_call():
                    response = cls._client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config={'temperature': temperature}
                    )
                    return response.text
                
                return await asyncio.wait_for(asyncio.to_thread(sync_call), timeout=timeout)
            
            except asyncio.TimeoutError:
                logger.warning(f"Gemini API timeout on attempt {attempt + 1}")
                if attempt == retries - 1:
                    raise HTTPException(status_code=504, detail="Gemini timeout")
                await asyncio.sleep(2 ** attempt) # Exponential backoff
            except errors.APIError as e:
                logger.warning(f"Gemini API Error on attempt {attempt + 1}: {e}")
                if attempt == retries - 1:
                    raise HTTPException(status_code=502, detail="Network error")
                await asyncio.sleep(2 ** attempt) # Exponential backoff
            except Exception as e:
                logger.error(f"Unexpected Gemini Error: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail="Network error")

    @classmethod
    def _parse_json_response(cls, text: str) -> any:
        """Extract JSON cleanly from AI output, stripping any markdown."""
        logger.debug(f"Raw AI Output: {text}")
        text = text.strip()
        # Remove markdown code blocks if present
        text = re.sub(r"^```json\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"^```\s*", "", text, flags=re.MULTILINE)
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {text}")
            raise HTTPException(status_code=422, detail="Invalid JSON") from e

    @classmethod
    async def chat(cls, prompt: str) -> str:
        """Handle conversation logic."""
        logger.info("Calling chat endpoint with Gemini")
        return await cls._generate(prompt, temperature=0.5)

    @classmethod
    async def extractComplaint(cls, prompt: str) -> dict:
        """Extract structured JSON complaint data from a text prompt."""
        logger.info("Calling extractComplaint endpoint with Gemini")
        result_text = await cls._generate(prompt, temperature=0.1)
        return cls._parse_json_response(result_text)

    @classmethod
    async def recommend(cls, prompt: str) -> list[dict]:
        """Generate a list of recommended schemes based on a profile."""
        logger.info("Calling recommend endpoint with Gemini")
        # Increase timeout specifically for recommendation
        result_text = await cls._generate(prompt, temperature=0.2, timeout=30.0)
        return cls._parse_json_response(result_text)
