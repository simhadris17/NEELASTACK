import json
from typing import Any

from packages.neelastack.database.models import AuditEvent


def record_audit(
    db,
    event_type: str,
    actor_id: int | str | None = None,
    resource_type: str | None = None,
    resource_id: int | str | None = None,
    details: dict[str, Any] | None = None,
) -> AuditEvent:
    event = AuditEvent(
        event_type=event_type,
        actor_id=str(actor_id) if actor_id is not None else None,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id is not None else None,
        details=json.dumps(details or {}, default=str),
    )
    db.add(event)
    return event
