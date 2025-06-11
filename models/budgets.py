import uuid

from sqlalchemy import Column, func, ForeignKey, DECIMAL, Date, Integer
from sqlalchemy import String, UUID, Boolean, DateTime
from sqlalchemy.orm import relationship

from core.base import Base


class Budgets(Base):
    __tablename__ = 'budgets'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    expense_type_id = Column(UUID, ForeignKey("expense_types.id"))
    expense_type = relationship('ExpenseTypes', back_populates='budgets')
    department_id = Column(UUID, ForeignKey("departments.id"))
    department = relationship('Departments', back_populates='budgets')
    start_date = Column(Date)
    finish_date = Column(Date)
    status = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    transactions = relationship('Transactions', back_populates='budget')
