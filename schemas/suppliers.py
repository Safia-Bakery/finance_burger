from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base_model import TunedModel



class Suppliers(TunedModel):
    id: UUID
    name: str
    is_active: Optional[bool]
    created_at: Optional[datetime]


class Supplier(Suppliers):
    description: Optional[str] = None
    updated_at: Optional[datetime] = None


class CreateSupplier(TunedModel):
    name: str
    description: Optional[str] = None


class UpdateSupplier(TunedModel):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
