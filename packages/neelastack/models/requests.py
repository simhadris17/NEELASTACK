from pydantic import BaseModel, EmailStr
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None
class AgentRunRequest(BaseModel):
    goal: str
