from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.booking import SiteVisitBooking
from app.services.container import (
    booking_service,
    conversation_service,
)


router = APIRouter(
    prefix="/api",
    tags=["bookings"],
)


class BookingRequest(BaseModel):
    session_id: str
    booking: SiteVisitBooking


@router.post("/bookings")
def book_site_visit(request: BookingRequest):

    session = conversation_service.get_session(
        request.session_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    result = booking_service.book_site_visit(
        request.booking
    )

    conversation_service.update_booking(
        request.session_id,
        result,
    )

    return result
