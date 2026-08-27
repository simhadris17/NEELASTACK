"""Server-side text-to-speech adapters."""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
from shutil import which

import httpx

from packages.neelastack.core.config import settings

from .base import TTSProvider


class LocalTTS(TTSProvider):
    name = "local"

    async def synthesize(self, text: str, voice: str | None = None) -> tuple[bytes, str]:
        command = which("espeak") or which("espeak-ng")
        if command:
            process = await asyncio.create_subprocess_exec(
                command, "-w", "-", text, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0 and stdout:
                return stdout, "audio/wav"
            raise RuntimeError(stderr.decode(errors="replace")[-1000:] or "local TTS failed")
        # pyttsx3 is optional and commonly available on desktop installations.
        try:
            import pyttsx3  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Local TTS is unavailable. Install espeak or the optional pyttsx3 package."
            ) from exc
        root = Path("voice_uploads")
        root.mkdir(exist_ok=True)
        path = root / f"{uuid.uuid4().hex}.wav"

        def render() -> None:
            engine = pyttsx3.init()
            if voice:
                engine.setProperty("voice", voice)
            engine.save_to_file(text, str(path))
            engine.runAndWait()

        await asyncio.to_thread(render)
        try:
            return path.read_bytes(), "audio/wav"
        finally:
            path.unlink(missing_ok=True)


class OpenAITTS(TTSProvider):
    name = "openai"

    async def synthesize(self, text: str, voice: str | None = None) -> tuple[bytes, str]:
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI TTS is not configured (OPENAI_API_KEY is missing)")
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.post(
                f"{settings.openai_base_url.rstrip('/')}/audio/speech",
                headers={"Authorization": "Bearer " + settings.openai_api_key},
                json={
                    "model": settings.openai_tts_model,
                    "voice": voice or settings.openai_tts_voice,
                    "input": text,
                    "response_format": "mp3",
                },
            )
            response.raise_for_status()
            return response.content, "audio/mpeg"


TTS_PROVIDERS = {"local": LocalTTS, "openai": OpenAITTS}


def get_tts_providers() -> list[TTSProvider]:
    names = [settings.tts_provider, *settings.voice_fallbacks.split(",")]
    return [TTS_PROVIDERS[n.strip().lower()]() for n in dict.fromkeys(names) if n.strip().lower() in TTS_PROVIDERS]
