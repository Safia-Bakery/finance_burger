import uuid

from sqlalchemy import Integer, BIGINT, String, DateTime, UUID, Boolean
from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.base import Base



class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    tg_id = Column(BIGINT, index=True, unique=True)
    fullname = Column(String)
    language = Column(String)
    phone = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    role_id = Column(UUID, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    role = relationship('Roles', back_populates='users')
    clients = relationship('Clients', back_populates='user', passive_deletes=True)
    logs = relationship('Logs', back_populates='user', passive_deletes=True)
    requests = relationship('Requests', back_populates='user', passive_deletes=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

