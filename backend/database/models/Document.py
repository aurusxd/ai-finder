from sqlalchemy import DECIMAL, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database.models.Base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(Text,nullable=False)
    size = Column(DECIMAL, nullable=False)
    name = Column(String(100),nullable=False)

    chat = relationship("Chat", back_populates="document")
    documentChunk = relationship("DocumentChunk", back_populates="document")
