from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.ai_schema import AiAnswerModel, AiModel
from backend.services.ollama_service import ollama_service

router = APIRouter(tags=["ai"], prefix="/ai")


@router.post(
    "/",
    response_model=AiAnswerModel,
    summary="Generate ai message",
    description="Generate a new message from user context",
    response_description="Created document object",
    responses={
        200: {"description": "The message was successfully generated"},
        400: {"description": "Error uploading the document"},
        403: {"description": "User doesn't exist"},
        409: {"description": "Document with this name already exists"},
    },
)
async def generate_message_from_context(
    data: AiModel,
    # current_user: Annotated[User, Depends(security.get_current_user)],
):
    message = await ollama_service.answer_by_context(data.question, data.context)
    return AiAnswerModel(
        question=data.question,
        context=data.context,
        answer=message,
    )
