from langchain_ollama import ChatOllama


class OlammaService:
    def __init__(self):
        self.llm = ChatOllama(
            model="qwen3",
            temperature=0.2,
        )

    async def ask(self, question: str):
        return self.llm.invoke(question)

    async def answer_by_context(self, question: str, context: str) -> str:

        prompt = f"""
            Контекст: {context}

            Вопрос: {question}

            Ответь только на основе контекста. Если ты не нашел ответ на вопрос в контексте то так и скажи, не надо придумывать или врать.
            """  # noqa: E501

        response = await self.llm.ainvoke(prompt)

        return response.content


ollama_service = OlammaService()
