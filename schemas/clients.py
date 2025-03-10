from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.base_model import TunedModel
from schemas.users import GetUsers



class Clients(TunedModel):
    id: UUID
    fullname: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool]
    created_at: Optional[datetime]



class Client(Clients):
    tg_id: Optional[int]
    language: Optional[str]
    updated_at: Optional[datetime] = None



class UpdateClient(TunedModel):
    id: UUID
    fullname: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    is_active: Optional[bool] = None
