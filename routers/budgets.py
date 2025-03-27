from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import ContractDAO, BudgetDAO
from schemas.budgets import Budgets, CreateBudget, Budget
from schemas.contracts import Contract, CreateContract
from utils.utils import PermissionChecker



budgets_router = APIRouter()




@budgets_router.post("/budgets", response_model=Budget)
async def create_budget(
        body: CreateBudget,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Budgets": ["create"]}))
):
    created_obj = await BudgetDAO.add(session=db, **body.model_dump())
    db.commit()
    db.refresh(created_obj)
    return created_obj



@budgets_router.get("/budgets", response_model=List[Budgets])
async def get_budget_list(
        department_id: UUID,
        start_date: date,
        finish_date: date,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Budgets": ["read"]}))
):
    filters = {
        "department_id": department_id,
        "start_date": start_date,
        "finish_date": finish_date
    }
    objs = await BudgetDAO.get_by_attributes(session=db, filters=filters)
    for obj in objs:
        budget = (await BudgetDAO.get_budget_sum(session=db, budget_id=obj.id))[0]
        obj.value = budget

    return objs



@budgets_router.get("/budgets/{id}", response_model=Budget)
async def get_budget(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Budgets": ["read"]}))
):
    obj = await BudgetDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return obj



