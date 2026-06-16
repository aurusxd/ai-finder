

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from backend.database.models.Base import Base


class DocumentChunk(Base):
    __tablename__ = "documentChunks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text,nullable=False)
    page = Column(Integer,nullable=False)
    chunk_index=Column(Integer,nullable=False)
    document_id = Column(
        Integer,ForeignKey("documents.id", ondelete="CASCADE"), nullable=False,
    )

    document = relationship("Document", back_populates="documentChunk")

