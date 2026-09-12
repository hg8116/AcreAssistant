from app.models.session import ConversationSession
from app.prompts.sales_agent import SYSTEM_PROMPT
from app.services.llm_service import LLMService


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
