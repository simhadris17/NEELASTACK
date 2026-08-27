from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.database.models import Tool
from packages.neelastack.database.session import get_db
from packages.neelastack.mcp.registry import registry
from packages.neelastack.security.audit import record_audit
from packages.neelastack.tools.db_handlers import get_db_tool_handler
from packages.neelastack.tools.executor import execute

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.get("")
def mcp_status(user=Depends(current_user)):
    return {
        "status": "ready",
        "protocol": "MCP-compatible local registry",
        "builtin_tools": len(registry.tools),
    }


@router.get("/tools")
def tools(db: Session = Depends(get_db), user=Depends(current_user)):
    builtin_tools = sorted(registry.tools)
    db_tools = db.scalars(
        select(Tool)
        .where(Tool.user_id == user.id, Tool.enabled.is_(True))
        .order_by(Tool.id.desc())
    ).all()
    return {
        "tools": builtin_tools,
        "db_tools": [
            {"id": tool.id, "name": tool.name, "tool_type": tool.tool_type,
             "config": tool.config, "enabled": tool.enabled}
            for tool in db_tools
        ],
    }


@router.post("/tools")
def register_tool(data: dict, db: Session = Depends(get_db), user=Depends(current_user)):
    name = data.get("name")
    tool_type = data.get("tool_type", "generic")
    config = data.get("config", {})
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=422, detail="Tool name is required")
    if name in registry.tools:
        raise HTTPException(status_code=409, detail="Cannot override a built-in tool")
    if not isinstance(tool_type, str) or not tool_type.strip():
        raise HTTPException(status_code=422, detail="Tool type is required")
    if not isinstance(config, dict):
        raise HTTPException(status_code=422, detail="Tool config must be an object")
    if get_db_tool_handler(tool_type) is None:
        raise HTTPException(status_code=422, detail=f"Unsupported tool type: {tool_type}")
    tool = Tool(user_id=user.id, name=name.strip(), tool_type=tool_type.strip(),
                config=config, enabled=True)
    db.add(tool)
    db.flush()
    record_audit(db, "mcp.tool.registered", user.id, "tool", tool.id, {"name": tool.name})
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Tool name is already registered") from exc
    db.refresh(tool)
    return {"id": tool.id, "name": tool.name, "tool_type": tool.tool_type,
            "config": tool.config, "enabled": tool.enabled}


@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    tool = db.scalar(select(Tool).where(Tool.id == tool_id, Tool.user_id == user.id))
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(tool)
    record_audit(db, "mcp.tool.deleted", user.id, "tool", tool_id)
    db.commit()
    return {"deleted": True, "tool_id": tool_id}


@router.post("/execute")
async def execute_tool(data: dict, db: Session = Depends(get_db), user=Depends(current_user)):
    name = data.get("name")
    args = data.get("args", {})
    if not name:
        raise HTTPException(status_code=422, detail="Tool name is required")
    if not isinstance(args, dict):
        raise HTTPException(status_code=422, detail="Tool args must be an object")

    if name in registry.tools:
        fn = registry.get(name)
        try:
            result = await execute(name, fn, **args)
        except PermissionError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        record_audit(db, "mcp.tool.executed", user.id, "tool", name)
        db.commit()
        return {"tool": name, "type": "builtin", "result": result}

    db_tool = db.scalar(select(Tool).where(Tool.name == name, Tool.user_id == user.id))
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    if not db_tool.enabled:
        raise HTTPException(status_code=403, detail="Tool is disabled")
    handler = get_db_tool_handler(db_tool.tool_type)
    if handler is None:
        raise HTTPException(status_code=501, detail=f"DB tool type '{db_tool.tool_type}' is not implemented")
    if "config" in args:
        raise HTTPException(status_code=422, detail="Tool config is managed by the database and cannot be supplied in args")
    try:
        result = await execute(db_tool.tool_type, handler, config=db_tool.config, **args)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    record_audit(db, "mcp.tool.executed", user.id, "tool", db_tool.id)
    db.commit()
    return {"tool": db_tool.name, "type": "db", "tool_type": db_tool.tool_type,
            "config": db_tool.config, "result": result}
