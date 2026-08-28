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
    name = (settings.model_provider or "openai").strip().lower()
    provider_class = PROVIDERS.get(name)

    if provider_class is None:
        raise RuntimeError(f"Unsupported model provider: {name}")

    return provider_class()


def get_provider_with_fallback():
    primary = (settings.model_provider or "openai").strip().lower()

    configured = [
        name.strip().lower()
        for name in (settings.provider_fallbacks or "").split(",")
        if name.strip()
    ]

    names = list(dict.fromkeys([primary, *configured]))

    providers = [
        PROVIDERS[name]()
        for name in names
        if name in PROVIDERS
    ]

    if not providers:
        raise RuntimeError("No configured model provider is available")

    return FallbackProvider(providers)
