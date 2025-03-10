from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.session import get_db
from dal.dao import PaymentTypeDAO
from schemas.payment_types import PaymentType, CreatePaymentType, PaymentTypes, UpdatePaymentType
from utils.utils import PermissionChecker


payment_types_router = APIRouter()



@payment_types_router.post("/payment-types", response_model=PaymentType)
async def create_payment_type(
        body: CreatePaymentType,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"PaymentTypes": ["create"]}))
):
    created_obj = await PaymentTypeDAO.add(session=db, **body.model_dump())
    await db.commit()
    await db.refresh(created_obj)
    return created_obj


@payment_types_router.get("/payment-types", response_model=List[PaymentTypes])
async def get_payment_type_list(
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"PaymentTypes": ["read"]}))
):
    objs = await PaymentTypeDAO.get_all(session=db)
    return objs


@payment_types_router.get("/payment-types/{id}", response_model=PaymentType)
async def get_payment_type(
        id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"PaymentTypes": ["read"]}))
):
    obj = await PaymentTypeDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return obj


@payment_types_router.put("/payment-types", response_model=PaymentType)
async def update_payment_type(
        body: UpdatePaymentType,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"PaymentTypes": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_obj = await PaymentTypeDAO.update(session=db, data=body_dict)
    await db.commit()
    await db.refresh(updated_obj)
    return updated_obj


@payment_types_router.delete("/payment-types", response_model=List[PaymentTypes])
async def delete_payment_type(
        id: Optional[UUID],
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"PaymentTypes": ["delete"]}))
):
    deleted_objs = await PaymentTypeDAO.delete(session=db, filters={"id": id})
    await db.commit()
    return deleted_objs

