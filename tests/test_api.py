from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "AcreAssistant API is running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_session():
    response = client.post("/api/sessions")

    assert response.status_code == 200

    data = response.json()

    assert "session_id" in data
    assert "messages" in data
    assert "lead" in data

def test_get_nonexistent_session():
    response = client.get(
        "/api/sessions/nonexistent-session/analytics"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
