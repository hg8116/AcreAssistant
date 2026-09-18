from enum import Enum


class ConversationOutcome(str, Enum):
    ONGOING = "ongoing"
    QUALIFIED_LEAD = "qualified_lead"
    SITE_VISIT_CONFIRMED = "site_visit_confirmed"
    FOLLOW_UP_REQUIRED = "follow_up_required"
    HUMAN_ESCALATION = "human_escalation"
    NOT_INTERESTED = "not_interested"
    OPTED_OUT = "opted_out"
    INCOMPLETE = "incomplete"
