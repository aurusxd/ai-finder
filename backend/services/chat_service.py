from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.chat import Chat
from backend.log import log
from depends import provider


class ChatService:
    @provider.inject_session
    async def create_chat(
        self,
        user_id: int,
        created_at: datetime = datetime.utcnow(),  # noqa: B008, DTZ003
        session: AsyncSession | None = None,
    ) -> Chat:
        # Исправлено: используем именованные аргументы
        chat = Chat(user_id=user_id, created_at=created_at)
        try:
            session.add(chat)
            await session.flush()
            await session.refresh(chat)
            log.info("Чат создан")
            return chat
        except SQLAlchemyError as e:
            log.exception("Ошибка создания чата: ", e)
            raise


chat_service = ChatService()
