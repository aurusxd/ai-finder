from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from backend.log import log
from backend.schemas.ai_schema import AiAnswerModel, AiModel
from backend.services.document_service import document_service
from backend.services.embedding_service import embedding_service
from backend.services.loader_service import loader_service
from backend.services.ollama_service import ollama_service
from backend.services.openAI_service import openai_service
from backend.services.openrouter_service import open_router
from backend.services.vector_store_service import vector_store_service
from depends import provider

router = APIRouter(tags=["ai"], prefix="/ai")
UPLOAD_DIR = Path("uploads")


@router.post(
    "/ask",
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
async def generate_message_from_context(  # noqa: PLR0913
    session: Annotated[AsyncSession, Depends(provider.get_session)],
    question: str = Form(...),
    user_id: int = Form(...),
    context: str = Form(""),
    document_id: int | None = Form(None),
    file: UploadFile | None = File(None),  # noqa: B008
):
    message_context = context
    active_document_id = document_id

    try:
        if file:
            content = await file.read()
            size = len(content)

            user_dir = UPLOAD_DIR / str(user_id)
            user_dir.mkdir(parents=True, exist_ok=True)

            file_path = user_dir / file.filename

            with open(file_path, "wb") as f:  # noqa: ASYNC230
                f.write(content)

            doc = await document_service.upload_document(
                user_id=user_id,
                name=file.filename,
                path=str(file_path),
                size=size,
                uploaded_at=datetime.utcnow(),  # noqa: DTZ003
                session=session,
            )

            if doc is None:
                raise HTTPException(status_code=500, detail="Document was not saved")

            active_document_id = doc.id

            # loader должен читать именно сохранённый файл
            chunks = await loader_service.document_loader(doc.id, session)

            collection_name = f"document_{doc.id}"
            # дальше: chunks -> embeddings -> ChromaDB
            await embedding_service.generate_embedding(
                chunks, document_name=collection_name
            )

            # потом ищем похожие чанки и собираешь context
            found_chunks = await vector_store_service.find_vectors(
                collection_name, question, 3
            )
            message_context = "\n\n".join(chunk.page_content for chunk in found_chunks)
        elif active_document_id:
            doc = await document_service.get_document_by_id(
                active_document_id,
                session=session,
            )

            if doc is None or doc.user_id != user_id:
                raise HTTPException(status_code=404, detail="Document was not found")

            collection_name = f"document_{active_document_id}"
            found_chunks = await vector_store_service.find_vectors(
                collection_name, question, 3
            )
            message_context = "\n\n".join(chunk.page_content for chunk in found_chunks)

        message = await ollama_service.answer_by_context(
            question=question,
            context=message_context,
        )

        log.info("Ответ получен")
        return AiAnswerModel(
            question=question,
            context=message_context,
            answer=message,
            document_id=active_document_id,
        )

    except httpx.ConnectError as exc:
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable.",
        ) from exc
