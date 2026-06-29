import json
import os

from dotenv import load_dotenv
from openrouter import OpenRouter
from backend.log import log
import requests

load_dotenv()

class OpenRouterService:

    async def answer_by_context(self, question: str, context: str) -> str:
        # First API call with reasoning
        key = os.getenv("OPENROUTER_API_KEY")
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "google/gemma-4-26b-a4b-it:free",
            "messages": [
                {
                "role": "user",
                "content": f"""
                    Ты AI-ассистент для поиска по документам.

                    Отвечай только на основе переданного контекста.
                    Если ответа нет в контексте, ответь:
                    "В документе нет информации для ответа."

                    Контекст:
                    {context}

                    Вопрос:
                    {question}
                    """,
                }
            ],
            "reasoning": {"enabled": True}
        })
        )

        # Extract the assistant message with reasoning_details
        response = response.json()
        return response["choices"][0]["message"]["content"]



open_router=OpenRouterService()
