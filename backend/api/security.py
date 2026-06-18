# backend/api/security.py
import base64
from typing import Annotated
import uuid

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.database.models.user import User
from depends import provider

bearer_scheme = HTTPBearer(auto_error=False)


def compress_token(uuid_str: str) -> str:
    """Сжимает UUID в base64 для cookie"""
    uid = uuid.UUID(uuid_str)
    binary_data = uid.bytes
    return base64.urlsafe_b64encode(binary_data).decode("utf-8").rstrip("=")


def decompress_token(compressed_str: str) -> str:
    """Разжимает base64 в UUID"""
    binary_data = base64.urlsafe_b64decode(compressed_str + "==")
    uid = uuid.UUID(bytes=binary_data)
    return str(uid)


class SecurityService:
    async def get_current_user(
        self,
        request: Request,
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(bearer_scheme),
        ] = None,
    ) -> User:
        user = await self._get_current_user(
            request=request,
            credentials=credentials,
        )
        provider.set_current_user(user=user)
        return user

    async def _get_current_user(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials | None,
    ) -> User:
        # Проверяем cookie
        browser_token = request.cookies.get("token")
        if browser_token:
            try:
                token = decompress_token(browser_token)
                return await self.authenticate(token)
            except Exception as e:
                print(f"Error decoding cookie token: {e}")

        # Проверяем Bearer токен
        if credentials and credentials.scheme.lower() == "bearer":
            token = credentials.credentials

            # Пробуем декомпрессировать, если это сжатый токен
            try:
                # Если токен выглядит как сжатый (короткий, нет дефисов)
                if len(token) < 30 and "-" not in token:
                    token = decompress_token(token)
            except Exception:
                pass  # Оставляем как есть - это обычный UUID

            return await self.authenticate(token)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    async def authenticate(
        self,
        token: str,
    ) -> User:
        """Аутентифицирует пользователя по токену"""
        try:
            token_uuid = uuid.UUID(token)
        except ValueError as err:
            raise HTTPException(
                status_code=403,
                detail="Invalid token format",
            ) from err



    def set_cookeis(
        self,
        token: str,
        response: Response,
    ):
        """Устанавливает сжатый токен в cookie"""
        response.set_cookie(
            key="token",
            value=compress_token(token),
            httponly=True,
            secure=True,
            samesite="lax",
        )

    def delete_cookeis(
        self,
        response: Response,
    ):
        response.delete_cookie(
            key="token",
            httponly=True,
            secure=True,
            samesite="lax",
        )


security = SecurityService()
