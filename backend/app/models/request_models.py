from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: list[ChatMessage] = []

class ComplaintRequest(BaseModel):
    complaint: str = Field(..., min_length=10)

class RecommendRequest(BaseModel):
    age: int = Field(..., gt=0)
    occupation: str = Field(..., min_length=1)
    monthly_income: int = Field(..., ge=0)
    state: str = Field(..., min_length=2)
