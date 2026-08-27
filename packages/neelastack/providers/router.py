from packages.neelastack.core.config import settings
from .ollama import OllamaProvider
from .openai import OpenAIProvider
from .groq import GroqProvider
from .fallback import FallbackProvider


PROVIDERS = {
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "groq": GroqProvider,
}


def get_provider():
    return PROVIDERS.get(settings.model_provider, OllamaProvider)()


def get_provider_with_fallback():
    configured = [name.strip().lower() for name in settings.provider_fallbacks.split(",") if name.strip()]
    names = [settings.model_provider.lower(), *configured]
    names = list(dict.fromkeys(names))
    providers = [PROVIDERS[name]() for name in names if name in PROVIDERS]
    if not providers:
        providers = [get_provider()]
    return FallbackProvider(providers)
