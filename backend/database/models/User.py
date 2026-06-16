from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database.models.Base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=False,unique=True)
    created_at = Column(DateTime, server_default=func.now())
    document_id = Column(
        Integer,ForeignKey("documents.id", ondelete="CASCADE"), nullable=False,
    )

    chat = relationship("Chat", back_populates="user")
    document = relationship("Document", back_populates="chat")


    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email_address}')>"
