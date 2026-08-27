import base64
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from typing import Any

from packages.neelastack.core.config import settings
from packages.neelastack.database.models import Job

HANDLERS: dict[str, Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]] = {}


def register_handler(
    kind: str, handler: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]] | None = None
):
    def decorator(fn: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]):
        HANDLERS[kind] = fn
        return fn
    return decorator(handler) if handler is not None else decorator


@register_handler("echo")
async def _echo(payload: dict[str, Any]) -> dict[str, Any]:
    return payload


@register_handler("chat")
async def _chat(payload: dict[str, Any]) -> dict[str, Any]:
    from packages.neelastack.providers.fallback import generate_with_fallback
    prompt = payload.get("prompt") or payload.get("message")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("chat jobs require a prompt")
    return {"answer": await generate_with_fallback(prompt, int(payload.get("max_tokens", 256)))}


@register_handler("stt")
async def _stt(payload: dict[str, Any]) -> dict[str, Any]:
    from packages.neelastack.voice.stt.adapters import get_stt_providers
    audio = base64.b64decode(payload["audio"])
    errors = []
    for provider in get_stt_providers():
        try:
            return {"text": await provider.transcribe(audio, payload.get("filename", "audio.wav"), payload.get("content_type", "")), "adapter": provider.name}
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError("; ".join(errors))


@register_handler("tts")
async def _tts(payload: dict[str, Any]) -> dict[str, Any]:
    from packages.neelastack.voice.tts.adapters import get_tts_providers
    errors = []
    for provider in get_tts_providers():
        try:
            audio, media_type = await provider.synthesize(payload["text"], payload.get("voice"))
            return {"audio": base64.b64encode(audio).decode(), "media_type": media_type, "adapter": provider.name}
        except Exception as exc:
            errors.append(str(exc))
    raise RuntimeError("; ".join(errors))


def create_job(db, user_id: int, kind: str, payload: dict, max_attempts: int | None = None) -> Job:
    job = Job(
        user_id=user_id, kind=kind, payload=payload, status="queued",
        max_attempts=max_attempts or settings.worker_max_attempts,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def job_response(job: Job) -> dict:
    return {
        "id": job.id,
        "kind": job.kind,
        "status": job.status,
        "payload": job.payload,
        "result": job.result,
        "error": job.error,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "available_at": job.available_at,
        "attempts": job.attempts,
        "max_attempts": job.max_attempts,
        "progress": job.progress,
    }


def mark_job(job: Job, status: str, result: dict | None = None, error: str | None = None) -> None:
    now = datetime.now(timezone.utc)
    job.status = status
    job.updated_at = now
    if status == "running":
        job.started_at = now
        job.attempts += 1
        job.progress = max(job.progress, 1)
    if status in {"completed", "failed", "cancelled"}:
        job.completed_at = now
        if status == "completed":
            job.progress = 100
    if result is not None:
        job.result = result
    job.error = error


def retry_job(job: Job, reset_attempts: bool = False) -> None:
    job.status = "queued"
    job.error = None
    job.completed_at = None
    job.started_at = None
    job.progress = 0
    job.available_at = datetime.now(timezone.utc)
    if reset_attempts:
        job.attempts = 0
