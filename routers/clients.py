from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core.session import get_db
from dal.dao import ClientDAO
from schemas.clients import Clients, Client, UpdateClient
from utils.utils import PermissionChecker



clients_router = APIRouter()




@clients_router.get("/clients", response_model=Page[Clients])
async def get_client_list(
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Clients": ["read"]}))
):
    objs = await ClientDAO.get_all(session=db)
    return paginate(objs)



@clients_router.get("/clients/{id}", response_model=Client)
async def get_client(
        id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Clients": ["read"]}))
):
    obj = await ClientDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return obj



@clients_router.put("/clients", response_model=Client)
async def update_client(
        body: UpdateClient,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Clients": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_obj = await ClientDAO.update(session=db, data=body_dict)
    await db.commit()
    await db.refresh(updated_obj)
    return updated_obj


