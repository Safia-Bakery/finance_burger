from datetime import datetime, date
from typing import Optional
from uuid import UUID
from schemas.base_model import TunedModel




class Cities(TunedModel):
    id: UUID
    name: str
    is_active: Optional[bool] = None
    created_at: Optional[datetime]


class City(Cities):
    limit: float = 0.0
    description: Optional[str] = None
    updated_at: Optional[datetime] = None


class CreateCity(TunedModel):
    name: str
    limit: float
    description: Optional[str] = None
    is_active: Optional[bool] = True
    country_id: UUID


class UpdateCity(CreateCity):
    id: UUID
    name: Optional[str] = None
    limit: Optional[float] = None
    country_id: Optional[UUID] = None
