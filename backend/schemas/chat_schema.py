from datetime import datetime

from pydantic import BaseModel


class ChatModel(BaseModel):
    id: int
    user_id: int
    created_at: datetime


class ChatCreateModel(BaseModel):
    user_id: int
    created_at: datetime
