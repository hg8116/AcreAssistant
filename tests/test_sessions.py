from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_session():
    response = client.post("/api/sessions")

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert "messages" in data
    assert "lead" in data
    assert "booking" in data
