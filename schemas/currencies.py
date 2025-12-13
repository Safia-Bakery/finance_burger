from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base_model import TunedModel


class Currencies(TunedModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime]



class Currency(Currencies):
    updated_at: Optional[datetime] = None



class CreateCurrency(TunedModel):
    name: str
    is_active: Optional[bool] = None


class UpdateCurrency(TunedModel):
    id: UUID
    name: Optional[str] = None
    is_active: Optional[bool] = None
