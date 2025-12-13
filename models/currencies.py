import uuid

from sqlalchemy import Integer, UUID, String, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column
from core.base import Base



class Currencies(Base):
    __tablename__ = 'currencies'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    requests = relationship('Requests', back_populates='currency', passive_deletes=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

