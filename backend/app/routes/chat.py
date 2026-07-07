from fastapi import APIRouter, HTTPException
from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse, StandardResponse
from app.services.ai_service import AIService
from app.services.scheme_service import SchemeService
from app.prompts.chat_prompt import build_chat_prompt
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=StandardResponse[ChatResponse])
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat interactions with the CivicAI assistant.
    Loads schemes and context, then generates an AI response.
    """
    try:
        schemes = SchemeService.get_all_schemes()
        prompt = build_chat_prompt(request.message, request.history, schemes)
        reply = await AIService.chat(prompt)
        return StandardResponse(
            success=True,
            message="Chat generated successfully.",
            data=ChatResponse(reply=reply)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process chat request.")
