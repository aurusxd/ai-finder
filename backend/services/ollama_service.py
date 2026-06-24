from langchain_ollama import ChatOllama


class OlammaService:
    def __init__(self):
        self.llm = ChatOllama(
            model="qwen3",
            temperature=0.2,
        )

    async def ask(self, question: str):
        return self.llm.invoke(question)

    def answer_by_context(self, question: str, context: str) -> str:

        prompt = f"""
            Контекст: {context}

            Вопрос: {question}

            Ответь только на основе контекста.
            """

        response = self._model.invoke(prompt)

        return response.content


ollama_service = OlammaService()
