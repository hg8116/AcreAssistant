from app.models.analytics import ConversationAnalytics
from app.models.outcome import ConversationOutcome
from app.models.session import ConversationSession


class AnalyticsService:

    def generate_analytics(
        self,
        session: ConversationSession,
    ) -> ConversationAnalytics:

        user_messages = sum(
            1
            for message in session.messages
            if message.role == "user"
        )

        assistant_messages = sum(
            1
            for message in session.messages
            if message.role == "assistant"
        )

        intents = [
            message.intent
            for message in []
        ]

        detected_intents = []

        if session.lead.intent:
            detected_intents.append(
                session.lead.intent.value
            )

        outcome = self._determine_outcome(session)

        return ConversationAnalytics(
            session_id=session.session_id,

            total_messages=len(session.messages),
            user_messages=user_messages,
            assistant_messages=assistant_messages,

            intents_detected=detected_intents,

            configuration=session.lead.configuration,
            budget=session.lead.budget,
            buying_purpose=session.lead.buying_purpose,
            purchase_timeline=session.lead.purchase_timeline,
            interest_level=session.lead.interest_level,

            site_visit_status=session.lead.site_visit_status,

            follow_up_required=session.lead.follow_up_required,
            human_escalation=session.lead.human_escalation,
            communication_opt_out=session.lead.communication_opt_out,

            conversation_outcome=outcome,
        )

    def _determine_outcome(
        self,
        session: ConversationSession,
    ) -> ConversationOutcome:

        lead = session.lead

        if lead.communication_opt_out:
            return ConversationOutcome.OPTED_OUT

        if session.booking.status.value == "confirmed":
            return ConversationOutcome.SITE_VISIT_CONFIRMED

        if lead.human_escalation:
            return ConversationOutcome.HUMAN_ESCALATION

        if lead.follow_up_required:
            return ConversationOutcome.FOLLOW_UP_REQUIRED

        if lead.intent and lead.intent.value == "not_interested":
            return ConversationOutcome.NOT_INTERESTED

        return ConversationOutcome.ONGOING
