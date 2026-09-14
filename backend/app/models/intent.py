from enum import Enum


class Intent(str, Enum):
    GENERAL_INQUIRY = "general_inquiry"
    PROJECT_INFORMATION = "project_information"
    REQUIREMENT = "requirement"
    PRICE_INQUIRY = "price_inquiry"
    OBJECTION = "objection"
    SITE_VISIT = "site_visit"
    FOLLOW_UP = "follow_up"
    BUSY = "busy"
    NOT_INTERESTED = "not_interested"
    OPT_OUT = "opt_out"
    HUMAN_ESCALATION = "human_escalation"
    UNKNOWN = "unknown"
