import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.booking import BookingStatus
from app.services.container import (
    agent_service,
    booking_service,
    conversation_service,
)


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["chat"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session = conversation_service.get_session(
        request.session_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    conversation_service.add_message(
        request.session_id,
        "user",
        request.message,
    )

    # Handle confirmation for an existing booking request.
    if (
        session.booking.status
        == BookingStatus.AWAITING_CONFIRMATION
        and agent_service.is_booking_confirmation(
            request.message
        )
    ):

        booking = agent_service.create_booking_from_session(
            session
        )

        result = booking_service.book_site_visit(
            booking
        )

        conversation_service.update_booking(
            request.session_id,
            result,
        )

        if result.status == BookingStatus.CONFIRMED:

            session.lead.site_visit_status = "confirmed"

            reply = (
                "Your site visit has been confirmed. "
                f"Your booking ID is {result.booking_id}."
            )

        else:

            session.lead.site_visit_status = "failed"

            reply = (
                "I'm sorry, I couldn't complete the "
                "site visit booking. "
                f"Reason: {result.failure_reason}"
            )

        conversation_service.add_message(
            request.session_id,
            "assistant",
            reply,
        )

        return ChatResponse(
            session_id=request.session_id,
            reply=reply,
        )

    # Extract lead information.
    try:

        extraction = agent_service.extract_lead(
            session
        )

        conversation_service.update_lead(
            request.session_id,
            extraction,
        )

        if extraction.intent:

            conversation_service.add_intent(
                request.session_id,
                extraction.intent.value,
            )

    except Exception:

        logger.exception(
            "Lead extraction failed"
        )

    # Generate the normal conversational response.
    reply = agent_service.respond(session)

    # Ask for booking confirmation when all details exist.
    if (
        agent_service.has_booking_details(session)
        and session.booking.status
        == BookingStatus.NOT_REQUESTED
    ):

        session.booking.status = (
            BookingStatus.AWAITING_CONFIRMATION
        )

        reply = (
            "I have the details for your site visit:\n"
            f"Name: {session.lead.name}\n"
            f"Date: {session.lead.preferred_date}\n"
            f"Time: {session.lead.preferred_time}\n\n"
            "Would you like me to confirm this booking?"
        )

    conversation_service.add_message(
        request.session_id,
        "assistant",
        reply,
    )

    return ChatResponse(
        session_id=request.session_id,
        reply=reply,
    )
