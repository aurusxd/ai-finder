from fastapi import APIRouter

from backend.schemas.chat_schema import ChatCreateModel, ChatModel
from backend.services.chat_service import chat_service

router = APIRouter(tags=["chat"], prefix="/chats")


@router.post(
    "/create",
    response_model=ChatModel,
    summary="Create a new chat",
    description="Create a new chat",
    response_description="Created document object",
    responses={
        200: {"description": "The chat was successfully created"},
        400: {"description": "Error uploading the document"},
        403: {"description": "User doesn't exist"},
        409: {"description": "Document with this name already exists"},
    },
)
async def create_a_new_chat(
    data: ChatCreateModel,
    # current_user: Annotated[User, Depends(security.get_current_user)],
):
    chat = await chat_service.create_chat(data.user_id, data.created_at)
    return ChatModel.model_validate(chat, from_attributes=True)


@router.get(
    "/user/{user_id}",
    response_model=list[ChatModel],
    summary="Get user chats",
    description="Get chat history for a user",
)
async def get_user_chats(user_id: int):
    chats = await chat_service.get_user_chats(user_id)
    return [ChatModel.model_validate(chat, from_attributes=True) for chat in chats]
