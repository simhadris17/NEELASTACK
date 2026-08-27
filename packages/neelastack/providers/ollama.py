import json
from collections.abc import AsyncIterator

import httpx

from packages.neelastack.core.config import settings
from packages.neelastack.providers.base import Provider


class OllamaProvider(Provider):
    async def generate(self, prompt: str, max_tokens: int = 256) -> str:
        async with httpx.AsyncClient(timeout=settings.ollama_timeout_seconds) as client:
            r = await client.post(
                f"{settings.ollama_base_url.rstrip('/')}/api/generate",
                json={
                    "model": settings.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "keep_alive": "30m",
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.2,
                    },
                },
            )
            r.raise_for_status()
            return r.json().get("response", "")

    async def stream(
        self, prompt: str, max_tokens: int = 256
    ) -> AsyncIterator[str]:
        async with httpx.AsyncClient(timeout=settings.ollama_timeout_seconds) as client:
            async with client.stream(
                "POST",
                f"{settings.ollama_base_url.rstrip('/')}/api/generate",
                json={
                    "model": settings.ollama_model,
                    "prompt": prompt,
                    "stream": True,
                    "keep_alive": "30m",
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.2,
                    },
                },
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    item = json.loads(line)
                    chunk = item.get("response", "")
                    if chunk:
                        yield chunk
                    if item.get("done"):
                        break
