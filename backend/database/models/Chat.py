from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from backend.database.models.Base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
    )
    message_id = Column(
        Integer,ForeignKey("messages.id", ondelete="CASCADE"), nullable=False,
    )

    user = relationship("User", back_populates="chat")
    message = relationship("Message", back_populates="chat")
