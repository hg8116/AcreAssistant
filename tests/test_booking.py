from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_successful_booking():
    session_response = client.post("/api/sessions")

    assert session_response.status_code == 200

    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/bookings",
        json={
            "session_id": session_id,
            "booking": {
                "name": "Test User",
                "phone": "9999999999",
                "preferred_date": "2026-10-25",
                "preferred_time": "11:00 AM",
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "confirmed"
    assert data["booking_id"] is not None
