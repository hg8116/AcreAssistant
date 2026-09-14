from openai import OpenAI

from app.core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)
from app.models.session import LeadExtraction


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

    def generate_response(
        self,
        system_prompt: str,
        messages: list[dict],
    ) -> str:

        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                *messages,
            ],
        )

        return response.choices[0].message.content

    def extract_lead(
        self,
        messages: list[dict],
    ) -> LeadExtraction:

        extraction_prompt = """
You are a structured data extraction system for a real-estate sales assistant.

Your ONLY output must be a valid JSON object.

Do not output:
- explanations
- markdown
- code fences
- safety labels
- comments
- conversational text

Return exactly these fields:

{
  "name": null,
  "phone": null,
  "configuration": null,
  "budget": null,
  "buying_purpose": null,
  "purchase_timeline": null,
  "interest_level": null,
  "follow_up_required": null,
  "follow_up_preference": null,
  "human_escalation": null,
  "communication_opt_out": null,
  "intent:": "unknown"
}

Use null when the information is not known.

Only extract information explicitly stated by the customer.
Do not guess or infer information.

Rules:
- "3 BHK" -> "3 BHK"
- "2 crore" -> "₹2 crore"
- Only mark communication_opt_out true when the customer clearly asks to stop communication.
- Only mark human_escalation true when the customer asks for a human representative.
- A question about the property does not automatically mean high interest.
- Do not invent contact information.

Return ONLY the JSON object.

Classify the customer's latest message into exactly one intent.

Available intents:

- general_inquiry
- project_information
- requirement
- price_inquiry
- objection
- site_visit
- follow_up
- busy
- not_interested
- opt_out
- human_escalation
- unknown

Intent definitions:

general_inquiry:
General conversation that does not fit another category.

project_information:
The customer is asking for factual information about the project.

requirement:
The customer is expressing what they want, such as configuration, budget, purpose, or timeline.

price_inquiry:
The customer is specifically asking about price, cost, affordability, discount, or payment amount.

objection:
The customer expresses a concern, hesitation, or resistance.

site_visit:
The customer wants to arrange, discuss, reschedule, or cancel a site visit.

follow_up:
The customer asks to be contacted later or provides a preferred follow-up time.

busy:
The customer says they are currently busy or cannot continue the conversation now.

not_interested:
The customer indicates they are not interested but does not explicitly ask to stop all communication.

opt_out:
The customer explicitly asks not to be contacted or communicated with anymore.

human_escalation:
The customer asks to speak with a human, salesperson, representative, or agent.

unknown:
The intent cannot be confidently classified.

The "intent" field must contain exactly one of the supported intent values.

Return ONLY a valid JSON object.
Do not return markdown, explanations, safety labels, or any other text.
"""

        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": extraction_prompt,
                },
                *messages,
            ],
            response_format={
                "type": "json_object",
            },
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Lead extraction returned an empty response")

        return LeadExtraction.model_validate_json(content)
