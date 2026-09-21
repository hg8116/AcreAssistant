from app.models.session import ConversationSession
from app.prompts.sales_agent import SYSTEM_PROMPT
from app.services.llm_service import LLMService
from app.models.booking import SiteVisitBooking

class AgentService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def respond(
        self,
        session: ConversationSession,
    ) -> str:

        messages = [
            message.model_dump()
            for message in session.messages
        ]

        return self.llm_service.generate_response(
            system_prompt=SYSTEM_PROMPT,
            messages=messages,
        )

    def extract_lead(
        self,
        session: ConversationSession,
    ):
        messages = [
            message.model_dump()
            for message in session.messages
        ]

        return self.llm_service.extract_lead(
            messages=messages,
        )

    def has_booking_details(self, session) -> bool:
        lead = session.lead

        return all([
            lead.name,
            lead.phone,
            lead.preferred_date,
            lead.preferred_time,
        ])

    def is_booking_confirmation(self, message: str) -> bool:
        confirmation_phrases = {
            "yes",
            "yes please",
            "confirm",
            "confirmed",
            "book it",
            "go ahead",
            "haan",
            "han",
            "ji haan",
            "kar do",
            "बुक कर दो",
        }

        normalized_message = message.strip().lower()

        return normalized_message in confirmation_phrases

    def create_booking_from_session(self, session):

        return SiteVisitBooking(
            name=session.lead.name,
            phone=session.lead.phone,
            preferred_date=session.lead.preferred_date,
            preferred_time=session.lead.preferred_time,
        )
