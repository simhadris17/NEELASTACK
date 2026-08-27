import asyncio
from collections.abc import AsyncIterator, Iterable

from packages.neelastack.core.config import settings

from .base import Provider


class FallbackProvider(Provider):
    """Try configured providers in order and retain the last useful error."""

    def __init__(self, providers: Iterable[Provider]):
        self.providers = list(providers)
        if not self.providers:
            raise ValueError("At least one provider is required")

    async def generate(self, prompt: str, max_tokens: int = 256) -> str:
        errors: list[Exception] = []
        for provider in self.providers:
            for attempt in range(max(1, settings.provider_max_retries + 1)):
                try:
                    answer = await provider.generate(prompt, max_tokens=max_tokens)
                    if answer:
                        return answer
                    raise RuntimeError(f"{provider.__class__.__name__} returned an empty response")
                except Exception as exc:
                    errors.append(exc)
                    if attempt < settings.provider_max_retries:
                        await asyncio.sleep(0.2 * (attempt + 1))
        raise RuntimeError("All model providers failed: " + "; ".join(str(e) for e in errors))

    async def stream(self, prompt: str, max_tokens: int = 256) -> AsyncIterator[str]:
        # Streaming failures before the first token can use the next provider.
        errors: list[Exception] = []
        for provider in self.providers:
            emitted = False
            try:
                async for chunk in provider.stream(prompt, max_tokens=max_tokens):
                    emitted = True
                    yield chunk
                return
            except Exception as exc:
                if emitted:
                    raise
                errors.append(exc)
        raise RuntimeError("All model providers failed: " + "; ".join(str(e) for e in errors))


async def generate_with_fallback(prompt: str, max_tokens: int = 256) -> str:
    from .router import get_provider_with_fallback

    return await get_provider_with_fallback().generate(prompt, max_tokens=max_tokens)
