from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base_model import TunedModel


class PayerCompanies(TunedModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime]


class PayerCompany(PayerCompanies):
    updated_at: Optional[datetime] = None


class CreatePayerCompany(TunedModel):
    name: str
    is_active: Optional[bool] = None



class UpdatePayerCompany(TunedModel):
    id: UUID
    name: Optional[str] = None
    is_active: Optional[bool] = None
