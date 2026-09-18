from datetime import datetime

from pydantic import BaseModel, Field


class ConversationAnalytics(BaseModel):
    session_id: str

    total_messages: int = 0
    user_messages: int = 0
    assistant_messages: int = 0

    intents_detected: list[str] = Field(default_factory=list)

    configuration: str | None = None
    budget: str | None = None
    buying_purpose: str | None = None
    purchase_timeline: str | None = None
    interest_level: str | None = None

    site_visit_status: str = "not_discussed"

    follow_up_required: bool = False
    human_escalation: bool = False
    communication_opt_out: bool = False

    conversation_outcome: str = "ongoing"

    generated_at: datetime = Field(
        default_factory=datetime.now
    )
