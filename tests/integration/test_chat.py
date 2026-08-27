def test_chat_route_exists():
    from apps.api.main import app
    assert any(getattr(r,'path','') == '/api/v1/chat' for r in app.routes)
