import os  # noqa: N999

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    async def answer_by_context(self, question: str, context: str) -> str:
        prompt = f"""
        Ты AI-ассистент для поиска по документам.

        Отвечай только на основе переданного контекста.
        Если ответа нет в контексте, скажи: "В документе нет информации для ответа."

        Контекст:
        {context}

        Вопрос:
        {question}
        """

        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text


openai_service = OpenAIService()
