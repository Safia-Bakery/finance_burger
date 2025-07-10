from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, NaiveDatetime

from schemas.base_model import TunedModel
from schemas.roles import GetRole


class GetUsers(TunedModel):
    id: UUID
    username: str
    tg_id: Optional[int] = None
    fullname: Optional[str] = None
    is_active: Optional[bool]
    created_at: Optional[datetime]



class GetUser(GetUsers):
    language: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    updated_at: Optional[datetime] = None
    role: Optional[GetRole] = None



class CreateUser(TunedModel):
    tg_id: Optional[int] = None
    fullname: Optional[str] = None
    language: Optional[str] = None
    phone: Optional[str] = None
    username: str
    password: str
    email: Optional[str] = None
    role_id: Optional[UUID] = None


class UpdateUser(TunedModel):
    id: UUID
    tg_id: Optional[int] = None
    fullname: Optional[str] = None
    language: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[UUID] = None


class LoginByPhone(TunedModel):
    phone: str
    password: str