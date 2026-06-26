from datetime import datetime, timezone
from hashlib import sha256
import uuid

from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.user import User
from backend.log import log
from backend.schemas.user_schema import LoginRequest, RegisterRequest
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
            return user
        except SQLAlchemyError as e:
            log.error("Пользователь не был зарегистрирован ", e)
            await session.rollback()
            return None

    @provider.inject_session
    async def register_new_user(
        self,
        session: AsyncSession,
        data: RegisterRequest,
    ) -> User | None:
        existing = await session.execute(
            select(User).where(
                or_(
                    User.username == data.username,
                    User.email_address == data.email_address,
                ),
            ),
        )
        if existing.scalar_one_or_none():
            return None

        user = User(
            username=data.username,
            password_hash=hash_password(data.password),
            email_address=data.email_address,
            created_at=datetime.now(timezone.utc),
            api_token=str(uuid.uuid4()),
        )
        return await self.register_user(user=user, session=session)

    @provider.inject_session
    async def get_user_by_token(
        self,
        session: AsyncSession,
        token: str,
    ) -> User | None:
        result = await session.execute(
            select(User).where(User.api_token == token),
        )
        return result.scalar_one_or_none()

    @provider.inject_session
    async def get_all_users(self, session: AsyncSession) -> list[User] | None:
        try:
            result = await session.execute(select(User).order_by(User.id))
            log.info("Пользователи получены..")
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            log.exception("Пользователи не были получены ", e)
            return None

    @provider.inject_session
    async def user_login(
        self,
        session: AsyncSession,
        payload: LoginRequest,
    ) -> User | None:
        result = await session.execute(
            select(User).where(
                or_(
                    User.username == payload.username,
                    User.email_address == payload.username,
                ),
            ),
        )
        user = result.scalar_one_or_none()
        if user is None or user.password_hash != hash_password(payload.password):
            log.info("Неправильное имя или пароль")
            return None
        log.info("Юзер найден")
        return user


user_service = UserService()
