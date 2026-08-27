def test_core_import():
    from packages.neelastack.core.config import settings
    assert settings.app_name == 'NEELASTACK'
