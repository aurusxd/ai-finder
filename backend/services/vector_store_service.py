from langchain_chroma import Chroma

from backend.database.models.document import Document
from backend.log import log


class VectorStoreService:
    async def find_vectors(
        self, collection_name: str, question: str, chunk_size: int
    ) -> list[Document]:
        """
        Ищет похожие вектор исходя из заданного вопроса

        Возвращает: список чанков

        """
        vector_store = Chroma(
            collection_name=collection_name,
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


vector_store_service = VectorStoreService()
