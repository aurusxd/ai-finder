import unicodedata

from anyio import Path as anyioPath
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.database.models.document import Document
from backend.log import log
from backend.services.document_service import document_service as ds


class DocumentLoader:
    async def document_loader(self, document_id: int) -> list[Document]:
        """
        Принимает документ айди и возвращает чанки документа.

        Возвращает: чанки документа

        """
        try:
            doc = await ds.get_document_by_id(document_id)

            raw_path = doc.path

            clean_path = "".join(
                ch for ch in raw_path if unicodedata.category(ch) != "Cf"
            ).strip()

            path = anyioPath(clean_path)

            if not path.exists():
                msg = f"Файл не найден: {str(path)!r}"
                raise FileNotFoundError(msg)

            loader = PyMuPDFLoader(str(path))
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=700,
                chunk_overlap=50,
            )

            chunks = text_splitter.split_documents(docs)

            log.info(f"Документ загружен и разбит на {len(chunks)} чанков")

            return chunks

        except Exception:
            log.exception("Ошибка при загрузке документа")
            raise


loader_service = DocumentLoader()
