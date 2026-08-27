from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import Tool
from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.tools.db_handlers import get_db_tool_handler

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("")
def list_tools(
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    tools = db.scalars(
        select(Tool)
        .where(Tool.user_id == user.id)
        .order_by(Tool.id.desc())
    ).all()

    return {
        "tools": [
            {
                "id": tool.id,
                "name": tool.name,
                "tool_type": tool.tool_type,
                "config": tool.config,
                "enabled": tool.enabled,
                "created_at": tool.created_at,
            }
            for tool in tools
        ]
    }


@router.post("")
def create_tool(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    name = data.get("name")
    tool_type = data.get("tool_type", "generic")
    config = data.get("config", {})
    enabled = data.get("enabled", True)

    if not name or not isinstance(name, str) or not name.strip():
        raise HTTPException(
            status_code=422,
            detail="Tool name is required",
        )

    if not isinstance(tool_type, str) or not tool_type.strip():
        raise HTTPException(
            status_code=422,
            detail="Tool type is required",
        )

    if not isinstance(config, dict):
        raise HTTPException(
            status_code=422,
            detail="Tool config must be an object",
        )

    tool_type = tool_type.strip()

    if tool_type != "generic" and get_db_tool_handler(tool_type) is None:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported tool type: {tool_type}",
        )

    existing = db.scalar(
        select(Tool).where(
            Tool.name == name.strip(),
            Tool.user_id == user.id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Tool already exists",
        )

    tool = Tool(
        user_id=user.id,
        name=name.strip(),
        tool_type=tool_type,
        config=config,
        enabled=bool(enabled),
    )

    db.add(tool)
    db.commit()
    db.refresh(tool)

    return {
        "id": tool.id,
        "name": tool.name,
        "tool_type": tool.tool_type,
        "config": tool.config,
        "enabled": tool.enabled,
        "created_at": tool.created_at,
    }


@router.get("/{tool_id}")
def get_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    tool = db.scalar(
        select(Tool).where(
            Tool.id == tool_id,
            Tool.user_id == user.id,
        )
    )

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found",
        )

    return {
        "id": tool.id,
        "name": tool.name,
        "tool_type": tool.tool_type,
        "config": tool.config,
        "enabled": tool.enabled,
        "created_at": tool.created_at,
    }


@router.patch("/{tool_id}")
def update_tool(
    tool_id: int,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    tool = db.scalar(
        select(Tool).where(
            Tool.id == tool_id,
            Tool.user_id == user.id,
        )
    )

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found",
        )

    if "name" in data:
        name = data.get("name")

        if not isinstance(name, str) or not name.strip():
            raise HTTPException(
                status_code=422,
                detail="Tool name is required",
            )

        name = name.strip()

        existing = db.scalar(
            select(Tool).where(
                Tool.name == name,
                Tool.user_id == user.id,
                Tool.id != tool_id,
            )
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Tool already exists",
            )

        tool.name = name

    if "tool_type" in data:
        tool_type = data.get("tool_type")

        if not isinstance(tool_type, str) or not tool_type.strip():
            raise HTTPException(
                status_code=422,
                detail="Tool type is required",
            )

        tool_type = tool_type.strip()

        if (
            tool_type != "generic"
            and get_db_tool_handler(tool_type) is None
        ):
            raise HTTPException(
                status_code=422,
                detail=f"Unsupported tool type: {tool_type}",
            )

        tool.tool_type = tool_type

    if "config" in data:
        config = data.get("config")

        if not isinstance(config, dict):
            raise HTTPException(
                status_code=422,
                detail="Tool config must be an object",
            )

        tool.config = config

    if "enabled" in data:
        tool.enabled = bool(data.get("enabled"))

    db.commit()
    db.refresh(tool)

    return {
        "id": tool.id,
        "name": tool.name,
        "tool_type": tool.tool_type,
        "config": tool.config,
        "enabled": tool.enabled,
        "created_at": tool.created_at,
    }


@router.delete("/{tool_id}")
def delete_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    tool = db.scalar(
        select(Tool).where(
            Tool.id == tool_id,
            Tool.user_id == user.id,
        )
    )

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found",
        )

    db.delete(tool)
    db.commit()

    return {
        "deleted": True,
        "tool_id": tool_id,
    }
