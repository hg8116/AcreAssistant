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
  "communication_opt_out": null
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
