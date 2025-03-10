from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.session import get_db
from dal.dao import SupplierDAO
from schemas.suppliers import Suppliers, Supplier, CreateSupplier, UpdateSupplier
from utils.utils import PermissionChecker



suppliers_router = APIRouter()




@suppliers_router.post("/suppliers", response_model=Supplier)
async def create_supplier(
        body: CreateSupplier,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Suppliers": ["create"]}))
):
    created_obj = await SupplierDAO.add(session=db, **body.model_dump())
    await db.commit()
    await db.refresh(created_obj)
    return created_obj



@suppliers_router.get("/suppliers", response_model=List[Suppliers])
async def get_supplier_list(
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Suppliers": ["read"]}))
):
    objs = await SupplierDAO.get_all(session=db)
    return objs



@suppliers_router.get("/suppliers/{id}", response_model=Supplier)
async def get_supplier(
        id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Suppliers": ["read"]}))
):
    obj = await SupplierDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return obj



@suppliers_router.put("/suppliers", response_model=Supplier)
async def update_supplier(
        body: UpdateSupplier,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Suppliers": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_obj = await SupplierDAO.update(session=db, data=body_dict)
    await db.commit()
    await db.refresh(updated_obj)
    return updated_obj



@suppliers_router.delete("/suppliers", response_model=List[Suppliers])
async def delete_supplier(
        id: Optional[UUID],
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Suppliers": ["delete"]}))
):
    deleted_objs = await SupplierDAO.delete(session=db, filters={"id": id})
    await db.commit()
    return deleted_objs

