import os

from dotenv import load_dotenv
import httpx

load_dotenv()


class OpenRouterService:
    async def answer_by_context(self, question: str, context: str) -> str:
        # First API call with reasoning
        key = os.getenv("OPENROUTER_API_KEY")

        payload = {
            "model": "nvidia/nemotron-3.5-content-safety:free",
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
                        """,  # noqa: RUF001
                }
            ],
            "reasoning": {"enabled": True},
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json=payload,  # httpx автоматически сериализует в JSON
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]


open_router = OpenRouterService()
