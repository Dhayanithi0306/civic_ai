# pyrefly: ignore [missing-import]
from fastapi import APIRouter, HTTPException, Path
from typing import List
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
import logging

from app.models.request_models import ComplaintRequest
from app.models.response_models import ComplaintResponse, StandardResponse
from app.services.ai_service import AIService
from app.services.complaint_service import ComplaintService
from app.prompts.complaint_prompt import build_complaint_prompt


logger = logging.getLogger(__name__)
router = APIRouter()

class ComplaintPatchRequest(BaseModel):
    status: str

@router.post("/", response_model=StandardResponse[ComplaintResponse])
async def create_complaint(request: ComplaintRequest):
    """
    Extract structured complaint data using AI and save it to the database.
    """
    try:
        prompt = build_complaint_prompt(request.complaint)
        extracted_data = await AIService.extractComplaint(prompt)
        
        extracted_data["category"] = extracted_data.get("category", "Other")
        extracted_data["location"] = extracted_data.get("location", "Unknown")
        extracted_data["severity"] = extracted_data.get("severity", "Medium")
        extracted_data["summary"] = extracted_data.get("summary", request.complaint[:100] + "...")

        saved_complaint = ComplaintService.save_complaint(extracted_data)
        return StandardResponse(
            success=True,
            message="Complaint filed successfully.",
            data=ComplaintResponse(**saved_complaint)
        )
    except ValueError as ve:
        logger.warning(f"Validation error in complaint extraction: {ve}")
        raise HTTPException(status_code=400, detail="Could not process the complaint accurately. Please try rephrasing.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create complaint endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process complaint.")

@router.get("/", response_model=StandardResponse[List[ComplaintResponse]])
async def get_complaints():
    """
    Retrieve all registered civic complaints.
    """
    complaints = ComplaintService.get_all_complaints()
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(complaints)} complaints.",
        data=[ComplaintResponse(**c) for c in complaints]
    )

@router.patch("/{complaint_id}", response_model=StandardResponse[ComplaintResponse])
async def update_complaint(complaint_id: str = Path(...), request: ComplaintPatchRequest = None):
    """
    Update the status of an existing complaint.
    """
    if not request:
        raise HTTPException(status_code=400, detail="Request body cannot be empty.")
    
    updated = ComplaintService.update_complaint_status(complaint_id, request.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    return StandardResponse(
        success=True,
        message="Complaint status updated.",
        data=ComplaintResponse(**updated)
    )
