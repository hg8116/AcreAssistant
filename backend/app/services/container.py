from app.services.agent_service import AgentService
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService


conversation_service = ConversationService()
llm_service = LLMService()

agent_service = AgentService(
    llm_service=llm_service
)
