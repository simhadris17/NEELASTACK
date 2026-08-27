"""Durable database-backed worker.

The queue works without Redis, while Redis can be used by deployments as a
wake-up/monitoring channel. Claiming is transactional so multiple replicas do
not process the same job on PostgreSQL.
"""

import asyncio
import time
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from packages.neelastack.core.config import settings
from packages.neelastack.database.base import Base
from packages.neelastack.database.models import Job
from packages.neelastack.database.session import SessionLocal, engine
from packages.neelastack.security.audit import record_audit
from packages.neelastack.workers.jobs import HANDLERS, mark_job, retry_job


def process_once() -> int:
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        stale_before = now - timedelta(seconds=settings.worker_job_timeout_seconds)
        stale_jobs = db.scalars(
            select(Job).where(Job.status == "running", Job.started_at < stale_before)
        ).all()
        for stale in stale_jobs:
            if stale.attempts < stale.max_attempts:
                retry_job(stale)
                stale.available_at = now
            else:
                mark_job(stale, "failed", error="Worker lease expired")
        db.commit()
        job = db.scalar(
            select(Job)
            .where(Job.status == "queued", Job.available_at <= now)
            .order_by(Job.id)
            .with_for_update(skip_locked=True)
        )
        if job is None:
            return 0
        mark_job(job, "running")
        db.commit()
        kind, payload, job_id = job.kind, job.payload, job.id
    finally:
        db.close()

    handler = HANDLERS.get(kind)
    try:
        if handler is None:
            raise ValueError(f"No handler registered for job kind '{kind}'")
        result = asyncio.run(asyncio.wait_for(handler(payload), settings.worker_job_timeout_seconds))
    except Exception as exc:
        db = SessionLocal()
        try:
            current = db.get(Job, job_id)
            if current is not None:
                mark_job(current, "failed", error=str(exc)[:4000])
                if current.attempts < current.max_attempts:
                    retry_job(current)
                    current.available_at = datetime.now(timezone.utc) + timedelta(
                        seconds=min(60, 2 ** current.attempts)
                    )
                record_audit(db, "job.failed", current.user_id, "job", current.id, {"error": str(exc)[:500]})
                db.commit()
        finally:
            db.close()
        return 1

    db = SessionLocal()
    try:
        current = db.get(Job, job_id)
        if current is not None and current.status != "cancelled":
            mark_job(current, "completed", result=result)
            record_audit(db, "job.completed", current.user_id, "job", current.id)
            db.commit()
    finally:
        db.close()
    return 1


def main() -> None:
    Base.metadata.create_all(engine)
    while True:
        processed = process_once()
        if not processed:
            time.sleep(settings.worker_poll_seconds)


if __name__ == "__main__":
    main()
