def test_provider_default():
    from packages.neelastack.providers.router import get_provider
    assert get_provider().__class__.__name__ == 'OllamaProvider'
