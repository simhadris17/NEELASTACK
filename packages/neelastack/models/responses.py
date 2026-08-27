from pydantic import BaseModel
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
class HealthResponse(BaseModel):
    status: str
