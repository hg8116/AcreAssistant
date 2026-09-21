from fastapi.testclient import TestClient

from app.main import app
from app.models.booking import BookingStatus
from app.services.container import conversation_service


client = TestClient(app)


def test_booking_endpoint_success():
    session = conversation_service.create_session()

    response = client.post(
        "/api/bookings",
        json={
            "session_id": session.session_id,
            "booking": {
                "name": "Test User",
                "phone": "9999999999",
                "preferred_date": "2026-10-25",
                "preferred_time": "11:00 AM"
            }
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "confirmed"
    assert data["booking_id"] is not None
