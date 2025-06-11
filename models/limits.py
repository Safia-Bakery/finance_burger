import uuid
from sqlalchemy import Column, func, DECIMAL, Date
from sqlalchemy import UUID, Boolean, DateTime
from core.base import Base




class Limits(Base):
    __tablename__ = 'limits'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    start_date = Column(Date)
    finish_date = Column(Date)
    value = Column(DECIMAL)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
