def test_health():
    from fastapi.testclient import TestClient
    from apps.api.main import app
    assert TestClient(app).get('/api/v1/health').status_code == 200
