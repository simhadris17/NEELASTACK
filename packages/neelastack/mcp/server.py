from fastapi import FastAPI
from packages.neelastack.mcp.schemas import ToolRequest
from packages.neelastack.mcp.registry import list_tools
app = FastAPI(title="NEELASTACK Local MCP")
@app.get("/tools")
def tools(): return {"tools": list_tools()}
@app.post("/call")
async def call(req: ToolRequest):
    if req.name == "echo": return {"ok": True, "result": req.arguments}
    return {"ok": False, "error": "Tool not registered"}
