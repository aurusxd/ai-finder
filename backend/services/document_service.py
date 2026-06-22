from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from backend.database.models.document import Document
from backend.log import log
from depends import AsyncSession, provider


class DocumentService:
    @provider.inject_session
    async def upload_document(  # noqa: PLR0913
        self,
        user_id: int,
        name: str,
        path: str,
        size: Decimal,
        uploaded_at: datetime,
        session: AsyncSession,
    ) -> Document | None:
        try:
            new_document = Document(
                name=name,
                path=path,
                size=size,
                uploaded_at=uploaded_at,
                user_id=user_id,
            )

            session.add(new_document)
            await session.commit()
            await session.refresh(new_document)
            log.info("Документ загружен")
            return new_document
        except SQLAlchemyError as e:
            log.critical(e)
            await session.rollback()
            return None

    @provider.inject_session
    async def get_document_by_id(self, document_id: int, session: AsyncSession) -> Document:  # noqa: E501
        try:
            result = await session.execute(select(Document).where(Document.id == document_id))  # noqa: E501
            log.info("Документ получен..")
            return list(await session.scalars(result).first())
        except SQLAlchemyError as e:
            log.exception("Документ не был получен ", e)
            return None






document_service = DocumentService()
