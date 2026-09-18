from fastapi import APIRouter, HTTPException

from app.services.container import (
    analytics_service,
    conversation_service,
)


router = APIRouter(
    prefix="/api/sessions",
    tags=["sessions"],
)

@router.post("")
def create_session():

    session = conversation_service.create_session()

    return session


@router.get("/{session_id}/analytics")
def get_analytics(session_id: str):

    session = conversation_service.get_session(
        session_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return analytics_service.generate_analytics(
        session
    )

@router.get("/{session_id}")
def get_session(session_id: str):

    session = conversation_service.get_session(
        session_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return session

