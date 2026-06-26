from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from backend.database.models.document import Document
from backend.log import log


class EmbeddingService:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    async def generate_embedding(
        self, chunks: list[Document], document_name: str
    ) -> bool:
        """
        Генерирует вектора c последующим их сохранением в chromaDB

        Возвращает: true-успешно, false-неуспешно

        """
        try:
            Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory="backend/database/chroma/chroma_db",
                collection_name=document_name,
            )
            return True
        except Exception as e:  # noqa: BLE001
            log.exception("Ошибка создания векторов: ", e)
            return False


embedding_service = EmbeddingService()
