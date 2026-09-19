from fastapi.testclient import TestClient

from app.main import app
from app.services.container import agent_service
from app.models.session import LeadExtraction

from app.models.intent import Intent


client = TestClient(app)


def test_chat_flow_with_mocked_llm(monkeypatch):
    def mock_respond(session):
        return "Northstar One mein 2 BHK ₹1.35 crore onwards se available hai."

    def mock_extract_lead(session):
        return LeadExtraction(
            configuration="2 BHK",
            budget="₹1.5 crore",
            intent=Intent.PRICE_INQUIRY,
        )

    monkeypatch.setattr(
        agent_service,
        "respond",
        mock_respond,
    )

    monkeypatch.setattr(
        agent_service,
        "extract_lead",
        mock_extract_lead,
    )

    session_response = client.post("/api/sessions")

    assert session_response.status_code == 200

    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/chat",
        json={
            "session_id": session_id,
            "message": "2 BHK ka price kya hai?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["session_id"] == session_id
    assert "₹1.35 crore" in data["reply"]

    session = client.get(
        f"/api/sessions/{session_id}"
    ).json()

    assert session["lead"]["configuration"] == "2 BHK"
    assert session["lead"]["budget"] == "₹1.5 crore"
    assert session["lead"]["intent"] == "price_inquiry"

def test_chat_with_invalid_session():
    response = client.post(
        "/api/chat",
        json={
            "session_id": "invalid-session",
            "message": "Hello",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
