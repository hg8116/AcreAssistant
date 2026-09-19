from pydantic import BaseModel, Field
from app.models.intent import Intent
from app.models.booking import SiteVisitBooking

class LeadExtraction(BaseModel):
    name: str | None = None
    phone: str | None = None

    configuration: str | None = None
    budget: str | None = None
    buying_purpose: str | None = None
    purchase_timeline: str | None = None

    interest_level: str | None = None

    follow_up_required: bool | None = None
    follow_up_preference: str | None = None

    human_escalation: bool | None = None
    communication_opt_out: bool | None = None

    intent: Intent | None = None

    preferred_date: str | None = None
    preferred_time: str | None = None

class LeadState(BaseModel):
    name: str | None = None
    phone: str | None = None

    configuration: str | None = None
    budget: str | None = None
    buying_purpose: str | None = None
    purchase_timeline: str | None = None

    interest_level: str | None = None
    
    intent: Intent | None = None

    site_visit_status: str = "not_discussed"

    follow_up_required: bool = False
    follow_up_preference: str | None = None

    human_escalation: bool = False
    communication_opt_out: bool = False

    conversation_status: str = "active"

    preferred_date: str | None = None
    preferred_time: str | None = None


class Message(BaseModel):
    role: str
    content: str


class ConversationSession(BaseModel):
    session_id: str
    messages: list[Message] = Field(default_factory=list)
    lead: LeadState = Field(default_factory=LeadState)
    booking: SiteVisitBooking = Field(
        default_factory=SiteVisitBooking
    )
    intent_history: list[str] = Field(default_factory=list)
