from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.database.models.document import Document
from backend.log import log
from backend.services.document_service import document_service as ds


class DocumentLoader:
    def document_loader(self, document_id: int) -> list[Document]:
        """
        Принимает документ айди и возвращает чанки документа.

        Возвращает: чанки документа

        """
        loader = PyMuPDFLoader(ds.get_document_by_id(document_id))
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
        return text_splitter.split_documents(docs)

loader_service = DocumentLoader()
