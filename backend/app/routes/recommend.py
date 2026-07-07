# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException
from app.models.request_models import RecommendRequest
from app.models.response_models import RecommendResponse, RecommendItem, StandardResponse
from app.services.ai_service import AIService
from app.services.scheme_service import SchemeService
from app.prompts.recommendation_prompt import build_recommendation_prompt
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=StandardResponse[RecommendResponse])
async def recommend_endpoint(request: RecommendRequest):
    """
    Generate tailored scheme recommendations based on user profile.
    """
    try:
        schemes = SchemeService.get_all_schemes()
        prompt = build_recommendation_prompt(
            age=request.age,
            occupation=request.occupation,
            income=request.monthly_income,
            state=request.state,
            schemes=schemes
        )
        
        recommendations_data = await AIService.recommend(prompt)
        
        if not isinstance(recommendations_data, list):
             raise ValueError("Expected a list of recommendations")

        items = []
        for rec in recommendations_data:
            items.append(RecommendItem(
                name=rec.get("name", "Unknown Scheme"),
                category=rec.get("category", "General"),
                eligibility_match_score=rec.get("eligibility_match_score", "Unknown"),
                reason=rec.get("reason", "Matches your profile."),
                benefits=rec.get("benefits", "Check official details."),
                documents_required=rec.get("documents_required", []),
                application_guidance=rec.get("application_guidance", "Visit the official portal.")
            ))
            
        if not items:
            raise HTTPException(status_code=404, detail="No matching schemes found.")

        return StandardResponse(
            success=True,
            message="Recommendations generated successfully.",
            data=RecommendResponse(recommendations=items)
        )
    except ValueError as ve:
        logger.warning(f"Validation error in recommendation: {ve}")
        raise HTTPException(status_code=400, detail="Could not generate valid recommendations from the AI response.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in recommendation endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process recommendation request.")
