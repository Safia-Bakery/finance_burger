from datetime import datetime, date
from typing import Optional
from uuid import UUID
from schemas.base_model import TunedModel




class Countries(TunedModel):
    id: UUID
    name: str
    is_active: Optional[bool] = None
    created_at: Optional[datetime]


class Country(Countries):
    description: Optional[str] = None
    updated_at: Optional[datetime] = None


class CreateCountry(TunedModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class UpdateCountry(CreateCountry):
    id: UUID
    name: Optional[str] = None
