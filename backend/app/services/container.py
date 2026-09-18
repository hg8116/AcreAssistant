from app.services.agent_service import AgentService
from app.services.booking_service import BookingService
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.analytics_service import AnalyticsService


conversation_service = ConversationService()
llm_service = LLMService()
booking_service = BookingService()
analytics_service = AnalyticsService()

agent_service = AgentService(
    llm_service=llm_service
)
