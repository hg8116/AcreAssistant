import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.container import (
    agent_service,
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

    reply = agent_service.respond(session)

    try:
        extraction = agent_service.extract_lead(session)

        conversation_service.update_lead(
            request.session_id,
            extraction,
        )

    except Exception:
        logger.exception("Lead extraction failed")

    conversation_service.add_message(
        request.session_id,
        "assistant",
        reply,
    )

    return ChatResponse(
        session_id=request.session_id,
        reply=reply,
    )
