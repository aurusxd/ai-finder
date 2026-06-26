from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    id: int
    username: str
    password_hash: str
    email_address: str
    created_at: datetime
    api_token: str


class UserByNameModel(BaseModel):
    username: str


class UserCreateModel(BaseModel):
    username: str
    password_hash: str
    email_address: str
    created_at: datetime
    api_token: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email_address: str
    created_at: datetime | None
    api_token: str


class RegisterRequest(BaseModel):
    username: str
    email_address: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email_address: str


class AuthResponse(BaseModel):
    message: str
    user: AuthUserRead
    api_token: str
