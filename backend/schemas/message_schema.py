from datetime import datetime

from pydantic import BaseModel


class MessageModel(BaseModel):
    id: int
    content: str
    role: str
    created_at: datetime
    chat_id: int


class MessageCreateModel(BaseModel):
    content: str
    role: str
    created_at: datetime
    chat_id: int
