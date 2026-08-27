from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import Tool
from packages.neelastack.auth.dependencies import current_user

from packages.neelastack.mcp.registry import registry
from packages.neelastack.tools.executor import execute
from packages.neelastack.tools.db_handlers import get_db_tool_handler


router = APIRouter(
    prefix="/mcp",
    tags=["mcp"],
)


@router.get("/tools")
def tools(
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    builtin_tools = sorted(registry.tools)

    db_tools = db.scalars(
        select(Tool)
        .where(
            Tool.user_id == user.id,
            Tool.enabled.is_(True),
        )
        .order_by(Tool.id.desc())
    ).all()

    return {
        "tools": builtin_tools,
        "db_tools": [
            {
                "id": tool.id,
                "name": tool.name,
                "tool_type": tool.tool_type,
                "config": tool.config,
                "enabled": tool.enabled,
            }
            for tool in db_tools
        ],
    }


@router.post("/execute")
async def execute_tool(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    name = data.get("name")
    args = data.get("args", {})

    if not name:
        raise HTTPException(
            status_code=422,
            detail="Tool name is required",
        )

    if not isinstance(args, dict):
        raise HTTPException(
            status_code=422,
            detail="Tool args must be an object",
        )

    # Built-in tool
    if name in registry.tools:
        fn = registry.get(name)

        try:
            result = await execute(
                name,
                fn,
                **args,
            )
        except PermissionError as e:
            raise HTTPException(
                status_code=403,
                detail=str(e),
            )

        return {
            "tool": name,
            "type": "builtin",
            "result": result,
        }

    # DB tool
    db_tool = db.scalar(
        select(Tool).where(
            Tool.name == name,
            Tool.user_id == user.id,
        )
    )

    if db_tool is None:
        raise HTTPException(
            status_code=404,
            detail="Tool not found",
        )

    if not db_tool.enabled:
        raise HTTPException(
            status_code=403,
            detail="Tool is disabled",
        )

    handler = get_db_tool_handler(db_tool.tool_type)

    if handler is None:
        raise HTTPException(
            status_code=501,
            detail=f"DB tool type '{db_tool.tool_type}' is not implemented",
        )

    if "config" in args:
        raise HTTPException(
            status_code=422,
            detail="Tool config is managed by the database and cannot be supplied in args",
        )

    try:
        result = await execute(
            db_tool.tool_type,
            handler,
            config=db_tool.config,
            **args,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )

    return {
        "tool": db_tool.name,
        "type": "db",
        "tool_type": db_tool.tool_type,
        "config": db_tool.config,
        "result": result,
    }
