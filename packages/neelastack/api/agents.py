from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import Agent
from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.models.requests import AgentRunRequest
from packages.neelastack.orchestration.runtime import AgentRuntime

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def list_agents(
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    agents = db.scalars(
        select(Agent)
        .where(Agent.user_id == user.id)
        .order_by(Agent.id.desc())
    ).all()

    return {
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "config_json": agent.config_json,
                "created_at": agent.created_at,
            }
            for agent in agents
        ]
    }


@router.post("")
def create_agent(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    name = data.get("name")

    if not name or not name.strip():
        raise HTTPException(
            status_code=422,
            detail="Agent name is required",
        )

    config_json = data.get("config_json", "{}")

    agent = Agent(
        user_id=user.id,
        name=name.strip(),
        config_json=config_json,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "id": agent.id,
        "name": agent.name,
        "config_json": agent.config_json,
        "created_at": agent.created_at,
    }


@router.get("/{agent_id}")
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    agent = db.scalar(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == user.id,
        )
    )

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return {
        "id": agent.id,
        "name": agent.name,
        "config_json": agent.config_json,
        "created_at": agent.created_at,
    }


@router.delete("/{agent_id}")
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    agent = db.scalar(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == user.id,
        )
    )

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    db.delete(agent)
    db.commit()

    return {
        "deleted": True,
        "agent_id": agent_id,
    }


@router.post("/run")
async def run_agent(
    data: AgentRunRequest,
    user=Depends(current_user),
):
    return await AgentRuntime().run(data.goal)
