from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base_model import TunedModel



class Buyers(TunedModel):
    id: UUID
    name: str
    is_active: Optional[bool]
    created_at: Optional[datetime]


class Buyer(Buyers):
    description: Optional[str] = None
    updated_at: Optional[datetime] = None


class CreateBuyer(TunedModel):
    name: str
    description: Optional[str] = None


class UpdateBuyer(TunedModel):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
