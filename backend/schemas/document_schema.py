from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class DocumentModel(BaseModel):
    id: int
    path: str
    size: Decimal
    name:str
    uploaded_at: datetime

class DocumentCreateModel(BaseModel):
    path: str
    size: Decimal
    name: str
    uploaded_at: datetime
    user_id: int

