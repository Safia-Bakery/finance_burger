from datetime import datetime
from typing import Optional, List
from uuid import UUID

from schemas.base_model import TunedModel
from schemas.budgets import Budget
from schemas.departments import Department
from schemas.requests import TransactionRequest


class Transactions(TunedModel):
    id: Optional[UUID] = None
    request: Optional[TransactionRequest] = None
    budget: Optional[Budget] = None
    status: Optional[int] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    is_income: Optional[bool] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None



class Transaction(Transactions):
    updated_at: Optional[datetime] = None



class CreateTransaction(TunedModel):
    request_id: Optional[UUID] = None
    budget_id: Optional[UUID] = None
    value: float
    status: Optional[int] = 5
    comment: Optional[str] = None


class PaginatedTransactions(TunedModel):
    page: int
    size: int
    pages: int
    total: int
    items: List[Transactions]


class DepartmentTransactions(TunedModel):
    department: Department
    transactions: PaginatedTransactions