import httpx
from packages.neelastack.core.config import settings
from packages.neelastack.providers.base import Provider

class OllamaProvider(Provider):
    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=180) as client:
            r = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            )
            r.raise_for_status()
            return r.json().get("response", "")
