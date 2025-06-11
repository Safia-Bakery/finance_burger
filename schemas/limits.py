from datetime import datetime, date
from typing import Optional
from uuid import UUID
from schemas.base_model import TunedModel




class Limits(TunedModel):
    id: UUID
    start_date: date
    finish_date: date
    value: Optional[float] = 0
    is_active: Optional[bool] = None
    created_at: Optional[datetime]


class Limit(Limits):
    updated_at: Optional[datetime] = None


class CreateLimit(TunedModel):
    start_date: date
    finish_date: date
    value: float


class UpdateLimit(CreateLimit):
    id: UUID
    is_active: Optional[bool] = None
