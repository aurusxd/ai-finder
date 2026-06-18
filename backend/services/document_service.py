from datetime import datetime
from decimal import Decimal

from backend.database.models.document import Document
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
            return new_document
        except Exception:
            await session.rollback()
            return None

document_service = DocumentService()
