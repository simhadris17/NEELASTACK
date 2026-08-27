from packages.neelastack.providers.base import Provider
class GroqProvider(Provider):
    async def generate(self, prompt: str) -> str:
        raise RuntimeError("Groq adapter is optional; no paid API is required by NEELASTACK.")
