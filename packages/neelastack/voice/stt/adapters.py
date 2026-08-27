"""Server-side speech-to-text adapters.

Optional local integrations are deliberately command based so the API remains
offline-safe and does not force a large ML runtime into the base install.
"""

from __future__ import annotations

import asyncio
import shlex
import uuid
from collections.abc import Callable
from pathlib import Path
from shutil import which

import httpx

from packages.neelastack.core.config import settings

from .base import STTProvider


class LocalSTT(STTProvider):
    name = "local"

    async def transcribe(
        self, audio: bytes, filename: str = "audio.wav", content_type: str = ""
    ) -> str:
        if content_type.startswith("text/") or filename.lower().endswith((".txt", ".text")):
            return audio.decode("utf-8", errors="replace")
        command = settings.whisper_command
        if not command:
            command = "whisper" if which("whisper") else None
        if not command:
            raise RuntimeError(
                "Local STT is unavailable. Configure WHISPER_COMMAND or install the whisper CLI."
            )
        root = Path("voice_uploads")
        root.mkdir(exist_ok=True)
        path = root / f"{uuid.uuid4().hex}{Path(filename).suffix or '.audio'}"
        try:
            await asyncio.to_thread(path.write_bytes, audio)
            args = shlex.split(command) + [
                str(path), "--model", settings.whisper_model,
                "--output_format", "txt", "--output_dir", str(root),
            ]
            process = await asyncio.create_subprocess_exec(
                *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), 300)
            if process.returncode != 0:
                raise RuntimeError(stderr.decode(errors="replace")[-1000:] or "whisper failed")
            transcript = stdout.decode(errors="replace").strip()
            txt_path = path.with_suffix(".txt")
            if txt_path.exists():
                transcript = txt_path.read_text(encoding="utf-8", errors="replace").strip()
                txt_path.unlink(missing_ok=True)
            return transcript
        finally:
            path.unlink(missing_ok=True)


class OpenAISTT(STTProvider):
    name = "openai"

    async def transcribe(self, audio: bytes, filename: str = "audio.wav", content_type: str = "") -> str:
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI STT is not configured (OPENAI_API_KEY is missing)")
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.post(
                f"{settings.openai_base_url.rstrip('/')}/audio/transcriptions",
                headers={"Authorization": "Bearer " + settings.openai_api_key},
                data={"model": settings.openai_stt_model, "response_format": "json"},
                files={"file": (filename, audio, content_type or "application/octet-stream")},
            )
            response.raise_for_status()
            return str(response.json().get("text", "")).strip()


class GroqSTT(STTProvider):
    name = "groq"

    async def transcribe(self, audio: bytes, filename: str = "audio.wav", content_type: str = "") -> str:
        if not settings.groq_api_key:
            raise RuntimeError("Groq STT is not configured (GROQ_API_KEY is missing)")
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.post(
                f"{settings.groq_base_url.rstrip('/')}/audio/transcriptions",
                headers={"Authorization": "Bearer " + settings.groq_api_key},
                data={"model": settings.groq_stt_model, "response_format": "json"},
                files={"file": (filename, audio, content_type or "application/octet-stream")},
            )
            response.raise_for_status()
            return str(response.json().get("text", "")).strip()


STT_PROVIDERS: dict[str, Callable[[], STTProvider]] = {
    "local": LocalSTT, "openai": OpenAISTT, "groq": GroqSTT
}


def get_stt_providers() -> list[STTProvider]:
    names = [settings.stt_provider, *settings.voice_fallbacks.split(",")]
    return [STT_PROVIDERS[n.strip().lower()]() for n in dict.fromkeys(names) if n.strip().lower() in STT_PROVIDERS]
