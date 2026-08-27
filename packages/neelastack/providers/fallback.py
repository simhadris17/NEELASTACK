from .router import get_provider
async def generate_with_fallback(prompt: str) -> str:
    return await get_provider().generate(prompt)
