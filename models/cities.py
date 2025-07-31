import uuid

from sqlalchemy import Column, ForeignKey, DateTime, func, Boolean, UUID
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from core.base import Base


class Cities(Base):
    __tablename__ = 'cities'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    country_id = Column(UUID, ForeignKey("countries.id", ondelete="SET NULL"), nullable=True)
    country = relationship('Countries', back_populates='cities')
    requests = relationship('Requests', back_populates='city', passive_deletes=True)
    limits = relationship('Limits', back_populates='city', passive_deletes=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

