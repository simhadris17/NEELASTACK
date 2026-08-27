from abc import ABC, abstractmethod


class STTProvider(ABC):
    name = "unknown"

    @abstractmethod
    async def transcribe(self, audio: bytes, filename: str = "audio.wav", content_type: str = "") -> str:
        """Return the transcript for an audio payload."""
