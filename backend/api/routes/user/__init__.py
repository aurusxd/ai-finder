from fastapi import APIRouter, HTTPException, Response, status

from backend.api.security import security
from backend.database.models.user import User
from backend.log import log
from backend.schemas.user_schema import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserByNameModel,
    UserRead,
)
from backend.services.user_service import user_service

router = APIRouter(tags=["User"], prefix="/users")


def _build_auth_response(user: User, message: str) -> AuthResponse:
    return AuthResponse(
        message=message,
        user=user,
        api_token=user.api_token,
    )


@router.post(
    "/register",
    response_model=AuthResponse,
    summary="Create a new user",
    responses={
        200: {"description": "The user was successfully created"},
        409: {"description": "User with this email or username already exists"},
    },
)
async def register_user(
    data: RegisterRequest,
    response: Response,
) -> AuthResponse:
    user = await user_service.register_new_user(data=data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists",
        )

    security.set_cookeis(user.api_token, response)
    log.info("Пользователь создан")
    return _build_auth_response(user, "Registration successful")


@router.post("/auth/login", response_model=AuthResponse)
async def login_user(
    payload: LoginRequest,
    response: Response,
) -> AuthResponse:
    user = await user_service.user_login(payload=payload)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    security.set_cookeis(user.api_token, response)
    return _build_auth_response(user, "Login successful")


@router.get("/users", response_model=list[UserRead])
async def list_users() -> list[User]:
    try:
        return await user_service.get_all_users()
    except Exception as e:
        log.exception("Пользователи не были получены", e)
        raise


@router.get("/userByName", response_model=UserRead)
async def get_by_name_user(username: str) -> User:
    try:
        return await user_service.get_user_by_name(username=username)
    except Exception as e:
        log.exception("Пользователь не были получены", e)
        raise
