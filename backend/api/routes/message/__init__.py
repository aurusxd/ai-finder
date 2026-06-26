from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.message_schema import MessageCreateModel, MessageModel
from backend.services.message_service import message_service
from depends import provider

router = APIRouter(tags=["message"], prefix="/messages")


@router.post(
    "/",
    response_model=MessageModel,
    summary="Create a new message",
    description="Generate a new message from user context",
    response_description="Created document object",
    responses={
        200: {"description": "The document was successfully uploaded"},
        400: {"description": "Error uploading the document"},
        403: {"description": "User doesn't exist"},
        409: {"description": "Document with this name already exists"},
    },
)
async def create_new_message(
    data: MessageCreateModel,
    # current_user: Annotated[User, Depends(security.get_current_user)],
):
    message = await message_service.create_message(
        data.content, data.role, data.chat_id
    )
    return MessageModel.model_validate(message, from_attributes=True)
