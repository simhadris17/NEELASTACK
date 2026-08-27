from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.core.config import settings
from packages.neelastack.voice.stt.adapters import get_stt_providers
from packages.neelastack.voice.tts.adapters import get_tts_providers

router = APIRouter(prefix="/voice", tags=["voice"])


def _configured(provider: str, kind: str) -> bool:
    if provider == "local":
        return bool(settings.whisper_command)
    if provider == "openai":
        return bool(settings.openai_api_key)
    if provider == "groq":
        return bool(settings.groq_api_key) and kind == "stt"
    return False


@router.get("")
def voice_status(user=Depends(current_user)):
    stt = get_stt_providers()
    tts = get_tts_providers()
    return {
        "status": "ready",
        "stt": {
            "available": any(_configured(p.name, "stt") for p in stt),
            "adapter": stt[0].name if stt else "none",
            "adapters": [p.name for p in stt],
        },
        "tts": {
            "available": any(_configured(p.name, "tts") for p in tts),
            "adapter": tts[0].name if tts else "none",
            "adapters": [p.name for p in tts],
        },
        "browser_fallback": True,
        "max_upload_bytes": settings.voice_max_upload_bytes,
    }


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...), user=Depends(current_user)):
    content = await file.read(settings.voice_max_upload_bytes + 1)
    if len(content) > settings.voice_max_upload_bytes:
        raise HTTPException(status_code=413, detail="Audio file exceeds the configured upload limit")
    if not content:
        raise HTTPException(status_code=422, detail="Audio file is empty")
    errors: list[str] = []
    for provider in get_stt_providers():
        try:
            text = await provider.transcribe(content, file.filename or "audio", file.content_type or "")
            return {"text": text, "adapter": provider.name}
        except Exception as exc:
            errors.append(f"{provider.name}: {exc}")
    raise HTTPException(
        status_code=503,
        detail="No STT adapter succeeded. " + " | ".join(errors),
        headers={"X-Voice-Fallback": "browser"},
    )


@router.post("/synthesize")
async def synthesize(data: dict, user=Depends(current_user)):
    text = data.get("text")
    if not isinstance(text, str) or not text.strip():
        raise HTTPException(status_code=422, detail="text is required")
    if len(text) > 20_000:
        raise HTTPException(status_code=422, detail="text is too long")
    voice = data.get("voice")
    errors: list[str] = []
    for provider in get_tts_providers():
        try:
            audio, media_type = await provider.synthesize(text.strip(), voice if isinstance(voice, str) else None)
            return Response(
                content=audio,
                media_type=media_type,
                headers={"X-Voice-Adapter": provider.name, "Content-Disposition": 'inline; filename="speech"'},
            )
        except Exception as exc:
            errors.append(f"{provider.name}: {exc}")
    raise HTTPException(
        status_code=503,
        detail="No TTS adapter succeeded. " + " | ".join(errors),
        headers={"X-Voice-Fallback": "browser"},
    )
