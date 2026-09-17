from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class BookingStatus(str, Enum):
    NOT_REQUESTED = "not_requested"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class SiteVisitBooking(BaseModel):
    booking_id: str | None = None

    name: str | None = None
    phone: str | None = None

    preferred_date: str | None = None
    preferred_time: str | None = None

    status: BookingStatus = BookingStatus.NOT_REQUESTED

    created_at: datetime | None = None
    failure_reason: str | None = None
