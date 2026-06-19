from datetime import datetime
from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.user import User
from backend.log import log
from depends import provider


def hash_password(raw_password: str) -> str:
    return sha256(raw_password.encode("utf-8")).hexdigest()


class UserService:
    @provider.inject_session
    async def create_test_user(
        self,
        session: AsyncSession | None = None,
    ) -> User:
        test_user = User(
            username="test",
            password_hash="test",  # noqa: S106
            email_address="test@mail.ru",
            created_at=datetime.utcnow(),  # noqa: DTZ003
            api_token="token",  # noqa: S106
            session=session,
        )
        session.add(test_user)
        await session.flush()
        await session.refresh(test_user)

    @provider.inject_session
    async def register_user(self, user: User, session: AsyncSession) -> User | None:
        try:
            session.add(user)
            log.info("Пользователь создан")
            await session.flush()
            await session.refresh(user)
        except SQLAlchemyError as e:
            log.error("Пользователь не был зарегистрирован ", e)
            await session.rollback()
            return None

    @provider.inject_session
    async def get_all_users(self, session: AsyncSession) -> list[User] | None:
        try:
            result = await session.execute(select(User).order_by(User.id))
            log.info("Пользователи получены..")
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            log.exception("Пользователи не были получены ", e)
            return None


user_service = UserService()
