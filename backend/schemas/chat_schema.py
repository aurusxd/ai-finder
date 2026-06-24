from datetime import datetime

from pydantic import BaseModel


class ChatModel(BaseModel):
    user_id: int
    created_at: datetime
