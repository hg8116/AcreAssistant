from app.models.booking import (
    BookingStatus,
    SiteVisitBooking,
)
from app.services.booking_service import BookingService


def test_successful_booking():
    service = BookingService()

    booking = SiteVisitBooking(
        name="Test User",
        phone="9999999999",
        preferred_date="2026-10-01",
        preferred_time="11:00 AM",
    )

    result = service.book_site_visit(booking)

    assert result.status == BookingStatus.CONFIRMED
    assert result.booking_id is not None
    assert result.created_at is not None


def test_booking_fails_without_phone():
    service = BookingService()

    booking = SiteVisitBooking(
        name="Test User",
        preferred_date="2026-10-01",
        preferred_time="11:00 AM",
    )

    result = service.book_site_visit(booking)

    assert result.status == BookingStatus.FAILED
    assert result.failure_reason == "Phone number is required"
