from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from backend.database.models.document import Document


class VectorService:
    async def generate_embedding(self, chunks: list[Document]) -> Chroma:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        return Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="backend/database/chroma/chroma_db",
            collection_name="documents",
        )


vector_service = VectorService()
