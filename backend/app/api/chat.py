from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.prompts.sales_agent import SYSTEM_PROMPT
# from app.services.conversation_service import ConversationService
# from app.services.llm_service import LLMService


from app.services.container import (
    agent_service,
    conversation_service,
    # llm_service,
)

router = APIRouter(prefix="/api", tags=["chat"])

# conversation_service = ConversationService()
# llm_service = LLMService()


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

    conversation_service.add_message(
        request.session_id,
        "assistant",
        reply,
    )

    return ChatResponse(
        session_id=request.session_id,
        reply=reply,
    )
