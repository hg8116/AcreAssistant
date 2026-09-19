from uuid import uuid4

from app.models.session import (
    ConversationSession,
    Message,
)


class ConversationService:
    def __init__(self):
        self.sessions: dict[str, ConversationSession] = {}

    def create_session(self) -> ConversationSession:
        session_id = str(uuid4())

        session = ConversationSession(
            session_id=session_id
        )

        self.sessions[session_id] = session

        return session

    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:

        return self.sessions.get(session_id)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> ConversationSession:

        session = self.sessions[session_id]

        session.messages.append(
            Message(
                role=role,
                content=content,
            )
        )

        return session

    def update_lead(
        self,
        session_id: str,
        extraction,
    ) -> ConversationSession:

        session = self.sessions[session_id]

        data = extraction.model_dump(exclude_none=True)

        for field, value in data.items():
            setattr(session.lead, field, value)

        return session

    def update_booking(
        self,
        session_id: str,
        booking,
    ) -> ConversationSession:

        session = self.sessions[session_id]

        session.booking = booking

        return session

    def add_intent(
        self,
        session_id: str,
        intent: str,
    ) -> ConversationSession:

        session = self.sessions[session_id]

        session.intent_history.append(intent)

        return session




