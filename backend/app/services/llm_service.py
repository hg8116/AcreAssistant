from openai import OpenAI

from app.core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)


class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        return response.choices[0].message.content
