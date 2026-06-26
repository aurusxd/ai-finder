from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.security import security
from backend.database.models.document import Document
from backend.database.models.user import User
from backend.log import log
from backend.schemas.document_schema import DocumentCreateModel, DocumentModel
from backend.services.document_service import document_service
from depends import provider

router = APIRouter(tags=["Document"], prefix="/documents")


@router.post(
    "/",
    response_model=DocumentModel,
    summary="Upload a new document",
    description="Uploads a document and binds it to the current user.",
    response_description="Created document object",
    responses={
        200: {"description": "The document was successfully uploaded"},
        400: {"description": "Error uploading the document"},
        403: {"description": "User doesn't exist"},
        409: {"description": "Document with this name already exists"},
    },
)
async def upload_document(
    data: DocumentCreateModel,
    # current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    # Получаем первого пользователя из БД
    result = await session.execute(select(User).limit(1))
    current_user = result.scalar_one_or_none()

    if not current_user:
        log.exception("Нету записей c пользователями в базе данных")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users in database. Please create a user first.",
        )

    document = await document_service.upload_document(
        path=data.path,
        name=data.name,
        size=Decimal(data.size) if data.size else Decimal(0),
        uploaded_at=datetime.now(timezone.utc),
        user_id=current_user.id,
        session=session,
    )

    if not document:
        log.exception("Документ не был загружен")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not created",
        )
    log.info("Документ загружен")
    return DocumentModel.model_validate(document, from_attributes=True)
