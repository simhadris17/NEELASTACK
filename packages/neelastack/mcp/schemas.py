from pydantic import BaseModel
class ToolRequest(BaseModel):
    name: str
    arguments: dict = {}
class ToolResponse(BaseModel):
    ok: bool
    result: object = None
    error: str | None = None
