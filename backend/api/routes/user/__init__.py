from contextlib import asynccontextmanager
from datetime import datetime, timezone
from hashlib import sha256
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.user import User
from backend.log import log
from backend.schemas.user_schema import UserCreateModel, UserModel, UserRead
from backend.services.user_service import user_service
from depends import provider

router = APIRouter(tags=["User"], prefix="/users")


@router.post(
    "/register",
    response_model=UserModel,
    summary="Create a new user",
    description="C",
    response_description="Created document object",
    responses={
        200: {"description": "The user was successfully created"},
        400: {"description": "Error user created"},
        403: {"description": "User doesn't exist"},
        409: {"description": "User with this email already exists"},
    },
)
async def register_user(
    data: UserCreateModel,
    # current_user: Annotated[User, Depends(security.get_current_user)],
):
    user = User(
        username=data.username,
        password_hash=data.password_hash,
        email_address=data.email_address,
        created_at=datetime.now(timezone.utc),
        api_token=data.api_token,
    )
    await user_service.register_user(user)

    if not user:
        log.exception("Пользователь не создан")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not created",
        )
    log.info("Пользователь создан")
    return UserModel.model_validate(user, from_attributes=True)


@router.get("/users", response_model=list[UserRead])
async def list_users() -> list[User]:
    try:
        return await user_service.get_all_users()
    except Exception as e:
        log.exception("Пользователи не были получены", e)
        raise
