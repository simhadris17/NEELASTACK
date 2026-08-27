import json
from collections.abc import AsyncIterator

import httpx

from packages.neelastack.core.config import settings
from packages.neelastack.providers.base import Provider


class OpenAIProvider(Provider):
    """OpenAI-compatible chat adapter. It also works with compatible gateways."""

    def _headers(self) -> dict[str, str]:
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI provider is not configured (OPENAI_API_KEY is missing)")
        return {
            "Authorization": "Bearer " + settings.openai_api_key,
            "Content-Type": "application/json",
        }

    def _payload(self, prompt: str, max_tokens: int, stream: bool = False) -> dict:
        return {
            "model": settings.openai_model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "stream": stream,
        }

    async def generate(self, prompt: str, max_tokens: int = 256) -> str:
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.post(
                f"{self._base_url().rstrip('/')}/chat/completions",
                headers=self._headers(),
                json=self._payload(prompt, max_tokens),
            )
            response.raise_for_status()
            choices = response.json().get("choices", [])
            return choices[0].get("message", {}).get("content", "") if choices else ""

    async def stream(self, prompt: str, max_tokens: int = 256) -> AsyncIterator[str]:
        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            async with client.stream(
                "POST",
                f"{self._base_url().rstrip('/')}/chat/completions",
                headers=self._headers(),
                json=self._payload(prompt, max_tokens, stream=True),
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line or line == "data: [DONE]":
                        continue
                    if line.startswith("data: "):
                        try:
                            item = json.loads(line[6:])
                        except json.JSONDecodeError:
                            continue
                        text = item.get("choices", [{}])[0].get("delta", {}).get("content")
                        if text:
                            yield text

    def _base_url(self) -> str:
        return settings.openai_base_url
