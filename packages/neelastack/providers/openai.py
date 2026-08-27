import httpx
from packages.neelastack.core.config import settings
from packages.neelastack.providers.base import Provider
class OpenAIProvider(Provider):
    async def generate(self, prompt: str) -> str:
        raise RuntimeError("OpenAI adapter is optional; configure your own implementation/key.")
