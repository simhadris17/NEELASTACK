from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=100_000)
    conversation_id: int | None = None
class AgentRunRequest(BaseModel):
    goal: str
    history: list[dict[str, str]] = Field(default_factory=list)
