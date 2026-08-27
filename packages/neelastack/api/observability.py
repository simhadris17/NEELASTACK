from fastapi import APIRouter, Depends, Query
from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.observability.state import metrics
from packages.neelastack.database.models import AuditEvent
from packages.neelastack.database.session import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/observability", tags=["observability"])


@router.get("")
def observability():
    snapshot = metrics.snapshot()
    return {
        "status": "ready",
        "metrics": {
            "requests": snapshot["requests"],
            "errors": snapshot["errors"],
            "average_latency_ms": snapshot["average_latency_ms"],
        },
        "telemetry": "in-process",
        "tracing": "request timing",
    }


@router.get("/metrics")
def get_metrics(user=Depends(current_user)):
    return metrics.snapshot()


@router.get("/events")
def get_events(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    events = db.scalars(
        select(AuditEvent).where(AuditEvent.actor_id == str(user.id)).order_by(AuditEvent.id.desc()).limit(limit)
    ).all()
    return {
        "events": [
            {"id": event.id, "event_type": event.event_type, "resource_type": event.resource_type,
             "resource_id": event.resource_id, "created_at": event.created_at}
            for event in events
        ]
    }
