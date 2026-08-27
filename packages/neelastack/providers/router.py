from packages.neelastack.core.config import settings
from .ollama import OllamaProvider
from .openai import OpenAIProvider
from .groq import GroqProvider
def get_provider():
    return {"ollama": OllamaProvider, "openai": OpenAIProvider, "groq": GroqProvider}.get(
        settings.model_provider, OllamaProvider
    )()
