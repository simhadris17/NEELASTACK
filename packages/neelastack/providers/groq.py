from packages.neelastack.core.config import settings
from packages.neelastack.providers.base import Provider
from packages.neelastack.providers.openai import OpenAIProvider


class GroqProvider(OpenAIProvider, Provider):
    """Groq's OpenAI-compatible API using its own credentials and model."""

    def _headers(self) -> dict[str, str]:
        if not settings.groq_api_key:
            raise RuntimeError("Groq provider is not configured (GROQ_API_KEY is missing)")
        return {
            "Authorization": "Bearer " + settings.groq_api_key,
            "Content-Type": "application/json",
        }

    def _payload(self, prompt: str, max_tokens: int, stream: bool = False) -> dict:
        payload = super()._payload(prompt, max_tokens, stream)
        payload["model"] = settings.groq_model
        return payload

    async def generate(self, prompt: str, max_tokens: int = 256) -> str:
        import httpx

        async with httpx.AsyncClient(timeout=settings.provider_timeout_seconds) as client:
            response = await client.post(
                f"{settings.groq_base_url.rstrip('/')}/chat/completions",
                headers=self._headers(),
                json=self._payload(prompt, max_tokens),
            )
            response.raise_for_status()
            choices = response.json().get("choices", [])
            return choices[0].get("message", {}).get("content", "") if choices else ""
    def _base_url(self) -> str:
        return settings.groq_base_url
