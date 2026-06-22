from langchain_community.document_loaders import PyMuPDFLoader
from log import log


class DocumentLoader:
    async def document_loader(self, document_id: int):
        loader = PyMuPDFLoader(self.ds.get_document_by_id(document_id))
        documents = loader.load()
        log.info(f"Страниц найдено: {len(documents)}")
