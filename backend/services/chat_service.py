from datetime import datetime

from sqlalchemy import desc, select
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

    @provider.inject_session
    async def get_user_chats(
        self,
        user_id: int,
        session: AsyncSession | None = None,
    ) -> list[Chat]:
        result = await session.execute(
            select(Chat)
            .where(Chat.user_id == user_id)
            .order_by(desc(Chat.created_at), desc(Chat.id))
        )
        return list(result.scalars().all())


chat_service = ChatService()
