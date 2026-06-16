from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, func
from sqlalchemy.orm import relationship

from backend.database.models.Base import Base



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255),nullable=False)
    role = Column(String(50),nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    chat_id = Column(
        Integer,ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )

    chat = relationship("Chat", back_populates="message")
