import base64
from typing import Annotated
import uuid

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.database.models.user import User
from depends import provider

bearer_scheme = HTTPBearer(auto_error=False)


def compress_token(uuid_str: str) -> str:
    uid = uuid.UUID(uuid_str)
    binary_data = uid.bytes
    return base64.urlsafe_b64encode(binary_data).decode("utf-8").rstrip("=")


def decompress_token(compressed_str: str) -> str:
    binary_data = base64.urlsafe_b64decode(compressed_str + "==")
    uid = uuid.UUID(bytes=binary_data)
    return str(uid)


class SecurityService:
    async def get_current_user(
        self,
        request: Request,
        credentials: Annotated[
            HTTPAuthorizationCredentials,
            Depends(bearer_scheme),
        ],
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
        credentials: HTTPAuthorizationCredentials,
    ) -> User:
        browser_token = request.cookies.get("token")
        if browser_token:
            return await self.authenticate_browser(
                token=decompress_token(browser_token),
            )

        if credentials and credentials.scheme.lower() == "bearer":
            return await self.authenticate(
                decompress_token(credentials.credentials),
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )

    async def authenticate(
        self,
        token: str,
    ) -> User:
        try:
            token_uuid = uuid.UUID(token)
        except ValueError as err:
            raise HTTPException(
                status_code=403,
                detail="Invalid token format",
            ) from err

        current_user = await User.get_by(api_token=token_uuid)

        if not current_user:
            raise HTTPException(status_code=403, detail="Token not found or expired")
        return current_user

    def set_cookeis(
        self,
        token: str,
        response: Response,
    ):
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
