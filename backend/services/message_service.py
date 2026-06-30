from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.message import Message
from backend.log import log
from depends import provider


class MessageService:
    @provider.inject_session
    async def create_message(
        self,
        content: str,
        role: str,
        chat_id: int,
        session: AsyncSession | None = None,
    ) -> Message:
        message = Message(content=content, role=role, chat_id=chat_id)
        try:
            session.add(message)
            await session.flush()
            await session.refresh(message)
            log.info("Сообщение создано")
            return message
        except SQLAlchemyError as e:
            log.exception("Ошибка создания сообщения: ", e)
            raise

    @provider.inject_session
    async def get_chat_messages(
        self,
        chat_id: int,
        session: AsyncSession | None = None,
    ) -> list[Message]:
        result = await session.execute(
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at, Message.id)
        )
        return list(result.scalars().all())


message_service = MessageService()
