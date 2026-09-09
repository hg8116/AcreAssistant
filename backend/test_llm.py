from app.prompts.sales_agent import SYSTEM_PROMPT
from app.services.llm_service import LLMService


def main():
    llm = LLMService()

    response = llm.generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_message="3 BHK ka starting price kya hai?"
    )

    print("\nAcreAssistant:")
    print(response)


if __name__ == "__main__":
    main()
