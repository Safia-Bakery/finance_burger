import uuid

from sqlalchemy import Column, ForeignKey, DateTime, func, UUID
from sqlalchemy.orm import relationship

from core.base import Base


class Receipts(Base):
    __tablename__ = 'receipts'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID, ForeignKey("requests.id", ondelete="SET NULL"), unique=True, nullable=True)
    request = relationship('Requests', back_populates='receipt') # lazy="selectin"
    file = relationship('Files', back_populates='receipt', passive_deletes=True) # lazy='selectin'
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

