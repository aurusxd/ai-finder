from datetime import datetime
from decimal import Decimal

from backend.database.models.document import Document
from backend.database.models.user import User
from depends import AsyncSession, provider


class DocumentService:
    @provider.inject_session
    async def upload_document(  # noqa: PLR0913
        self,
        current_user: User,
        name: str,
        file_path: str,
        file_size: Decimal,
        uploaded_at: datetime,
        session: AsyncSession,

    ) -> Document:
        new_document = Document(
            name=name,
            file_path=file_path,
            file_size=file_size,
            uploaded_at=uploaded_at,
            user_id=current_user.id,
        )
        if new_document:
            await session.commit()
            return new_document
        return None

document_service = DocumentService()
