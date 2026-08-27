from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from packages.neelastack.providers.streaming import stream_text
class Provider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 256) -> str: ...

    async def stream(
        self, prompt: str, max_tokens: int = 256
    ) -> AsyncIterator[str]:
        answer = await self.generate(prompt, max_tokens=max_tokens)
        async for chunk in stream_text(answer):
            yield chunk
