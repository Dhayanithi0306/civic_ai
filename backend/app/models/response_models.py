from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional, Any

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """Standardized API response wrapper."""
    success: bool = Field(..., description="Indicates if the request was successful.")
    message: str = Field(..., description="Human-readable message regarding the response.")
    data: Optional[T] = Field(None, description="The payload of the response, if successful.")
    error: Optional[str] = Field(None, description="Error details, if the request failed.")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="The AI assistant's conversational response.")

class ComplaintResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the complaint.")
    status: str = Field(..., description="Current status of the complaint.")
    timestamp: str = Field(..., description="ISO 8601 timestamp of creation.")
    summary: str = Field(..., description="A clear, concise one-sentence summary.")
    category: str = Field(..., description="Standardized civic category.")
    severity: str = Field(..., description="Severity level: Low, Medium, or High.")
    location: str = Field(..., description="The location mentioned in the complaint.")

class RecommendItem(BaseModel):
    name: str = Field(..., description="Exact name of the scheme.")
    category: str = Field(..., description="Category of the scheme.")
    eligibility_match_score: str = Field(..., description="High, Medium, or Low match.")
    reason: str = Field(..., description="Explicit explanation of why it matches the profile.")
    benefits: str = Field(..., description="Key benefits provided by the scheme.")
    documents_required: List[str] = Field(..., description="List of required documents.")
    application_guidance: str = Field(..., description="Brief steps on how to apply.")

class RecommendResponse(BaseModel):
    recommendations: List[RecommendItem] = Field(..., description="List of matched schemes.")
