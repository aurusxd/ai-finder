from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.security import security
from backend.database.models.document import Document
from backend.database.models.user import User
from backend.schemas.document_schema import DocumentCreateModel, DocumentModel
from backend.services.document_service import document_service
from depends import Provider, provider

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
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    if await Document.get_by(owner_id=current_user.id, session=session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can create only 1 customer",
        )

    if customer := await document_service.upload_document(
        current_user=current_user,
        name=data.name,
        description=data,
        session=session,
    ):
        return DocumentModel.model_validate(customer, from_attributes=True)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not created")
