from datetime import datetime
from uuid import uuid4

from app.models.booking import (
    BookingStatus,
    SiteVisitBooking,
)


class BookingService:

    def book_site_visit(
        self,
        booking: SiteVisitBooking,
    ) -> SiteVisitBooking:

        if not booking.name:
            return booking.model_copy(
                update={
                    "status": BookingStatus.FAILED,
                    "failure_reason": "Name is required",
                }
            )

        if not booking.phone:
            return booking.model_copy(
                update={
                    "status": BookingStatus.FAILED,
                    "failure_reason": "Phone number is required",
                }
            )

        if not booking.preferred_date:
            return booking.model_copy(
                update={
                    "status": BookingStatus.FAILED,
                    "failure_reason": "Preferred date is required",
                }
            )

        if not booking.preferred_time:
            return booking.model_copy(
                update={
                    "status": BookingStatus.FAILED,
                    "failure_reason": "Preferred time is required",
                }
            )

        return booking.model_copy(
            update={
                "booking_id": str(uuid4()),
                "status": BookingStatus.CONFIRMED,
                "created_at": datetime.now(),
                "failure_reason": None,
            }
        )
