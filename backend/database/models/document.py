from sqlalchemy import (
    DECIMAL,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from backend.database.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(Text, nullable=False)
    size = Column(DECIMAL, nullable=False)
    name = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    document_chunk = relationship("DocumentChunk", back_populates="document")
    user = relationship("User", back_populates="documents")
