from fastapi import APIRouter

from backend.schemas.message_schema import MessageCreateModel, MessageModel
from backend.services.message_service import message_service

router = APIRouter(tags=["message"], prefix="/messages")


@router.post(
    "/create",
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


@router.get(
    "/chat/{chat_id}",
    response_model=list[MessageModel],
    summary="Get chat messages",
    description="Get messages for a chat",
)
async def get_chat_messages(chat_id: int):
    messages = await message_service.get_chat_messages(chat_id)
    return [
        MessageModel.model_validate(message, from_attributes=True)
        for message in messages
    ]
