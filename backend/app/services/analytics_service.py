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

        detected_intents = session.intent_history.copy()

        completed_fields, completeness_percentage = (
            self._calculate_qualification_completeness(session)
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

            qualification_fields_completed=completed_fields,
            qualification_fields_total=5,
            qualification_completeness_percentage=(
                completeness_percentage
            ),

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

    def _calculate_qualification_completeness(
        self,
        session: ConversationSession,
    ) -> tuple[int, float]:

        lead = session.lead

        qualification_fields = [
            lead.configuration,
            lead.budget,
            lead.buying_purpose,
            lead.purchase_timeline,
            lead.interest_level,
        ]

        completed_fields = sum(
            1
            for field in qualification_fields
            if field is not None and str(field).strip()
        )

        total_fields = len(qualification_fields)

        percentage = (
            completed_fields / total_fields
        ) * 100

        return completed_fields, percentage
