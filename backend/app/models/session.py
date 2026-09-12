from pydantic import BaseModel, Field

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

class LeadState(BaseModel):
    name: str | None = None
    phone: str | None = None

    configuration: str | None = None
    budget: str | None = None
    buying_purpose: str | None = None
    purchase_timeline: str | None = None

    interest_level: str | None = None

    site_visit_status: str = "not_discussed"

    follow_up_required: bool = False
    follow_up_preference: str | None = None

    human_escalation: bool = False
    communication_opt_out: bool = False

    conversation_status: str = "active"


class Message(BaseModel):
    role: str
    content: str


class ConversationSession(BaseModel):
    session_id: str
    messages: list[Message] = Field(default_factory=list)
    lead: LeadState = Field(default_factory=LeadState)
