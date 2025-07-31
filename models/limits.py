import uuid
from sqlalchemy import Column, func, DECIMAL, Date, ForeignKey
from sqlalchemy import UUID, Boolean, DateTime
from sqlalchemy.orm import relationship

from core.base import Base




class Limits(Base):
    __tablename__ = 'limits'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    start_date = Column(Date)
    finish_date = Column(Date)
    value = Column(DECIMAL)
    city_id = Column(UUID, ForeignKey("cities.id", ondelete="SET NULL"), nullable=True)
    city = relationship('Cities', back_populates='limits')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
