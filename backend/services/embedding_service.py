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
            log.excpetion("Ошибка создания векторов: ", e)
            return False

    async def find_vectors(self: str, question: str, chunk_size: int) -> list[Document]:
        """
        Ищет похожие вектор исходя из заданного вопроса

        Возвращает: список чанков

        """
        vector_store = Chroma(
            collection_name=self,
            persist_directory="backend/database/chroma/chroma_db",
            embedding_function=self.embeddings,
        )
        try:
            return vector_store.similarity_search(
                question,
                k=chunk_size,
            )
        except Exception as e:
            log.exception("Ошибка поиска векторов: ", e)
            raise


embedding_service = EmbeddingService()
