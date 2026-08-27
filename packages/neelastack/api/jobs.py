from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.database.models import Job
from packages.neelastack.database.session import get_db
from packages.neelastack.security.audit import record_audit
from packages.neelastack.workers.jobs import create_job, job_response, retry_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def list_jobs(db: Session = Depends(get_db), user=Depends(current_user)):
    jobs = db.scalars(
        select(Job).where(Job.user_id == user.id).order_by(Job.id.desc()).limit(100)
    ).all()
    return {"jobs": [job_response(job) for job in jobs]}


@router.post("")
def enqueue_job(data: dict, db: Session = Depends(get_db), user=Depends(current_user)):
    kind = data.get("kind")
    payload = data.get("payload", {})
    if not isinstance(kind, str) or not kind.strip():
        raise HTTPException(status_code=422, detail="Job kind is required")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="Job payload must be an object")
    max_attempts = data.get("max_attempts")
    if max_attempts is not None and (not isinstance(max_attempts, int) or not 1 <= max_attempts <= 10):
        raise HTTPException(status_code=422, detail="max_attempts must be between 1 and 10")
    job = create_job(db, user.id, kind.strip(), payload, max_attempts)
    record_audit(db, "job.queued", user.id, "job", job.id, {"kind": job.kind})
    db.commit()
    return job_response(job)


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    job = db.scalar(select(Job).where(Job.id == job_id, Job.user_id == user.id))
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_response(job)


@router.post("/{job_id}/retry")
def retry(job_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    job = db.scalar(select(Job).where(Job.id == job_id, Job.user_id == user.id))
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status not in {"failed", "cancelled"}:
        raise HTTPException(status_code=409, detail="Only failed or cancelled jobs can be retried")
    retry_job(job, reset_attempts=True)
    record_audit(db, "job.retried", user.id, "job", job.id)
    db.commit()
    return job_response(job)


@router.post("/{job_id}/cancel")
def cancel(job_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
    job = db.scalar(select(Job).where(Job.id == job_id, Job.user_id == user.id))
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status not in {"queued", "running"}:
        raise HTTPException(status_code=409, detail="Job is already finished")
    job.status = "cancelled"
    job.completed_at = datetime.now(timezone.utc)
    record_audit(db, "job.cancelled", user.id, "job", job.id)
    db.commit()
    return job_response(job)
