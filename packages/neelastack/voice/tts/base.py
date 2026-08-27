from abc import ABC, abstractmethod


class TTSProvider(ABC):
    name = "unknown"

    @abstractmethod
    async def synthesize(self, text: str, voice: str | None = None) -> tuple[bytes, str]:
        """Return audio bytes and their MIME type."""
