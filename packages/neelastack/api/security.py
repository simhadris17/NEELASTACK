import json

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.core.config import settings
from packages.neelastack.database.models import AuditEvent
from packages.neelastack.database.session import get_db

router = APIRouter(prefix="/security", tags=["security"])


@router.get("")
def security(user=Depends(current_user)):
    return {
        "status": "enabled",
        "authentication": "jwt",
        "authorization": "user-scoped resources",
        "rate_limiting": {
            "requests": settings.rate_limit_requests,
            "window_seconds": settings.rate_limit_window_seconds,
            "backend": "redis" if settings.rate_limit_use_redis else "in-memory",
        },
        "audit_logging": True,
        "configured_providers": {
            "ollama": bool(settings.ollama_base_url and settings.ollama_model),
            "openai": bool(settings.openai_api_key),
            "groq": bool(settings.groq_api_key),
        },
    }


@router.get("/audit")
def audit_log(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    events = db.scalars(
        select(AuditEvent)
        .where(AuditEvent.actor_id == str(user.id))
        .order_by(AuditEvent.id.desc())
        .limit(limit)
    ).all()
    return {
        "events": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "resource_type": event.resource_type,
                "resource_id": event.resource_id,
                "details": json.loads(event.details or "{}"),
                "created_at": event.created_at,
            }
            for event in events
        ]
    }
