from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import LimitDAO
from schemas.limits import CreateLimit, Limits, Limit, UpdateLimit
from utils.utils import PermissionChecker



limits_router = APIRouter()




@limits_router.post("/limits")
async def create_limit(
        body: CreateLimit,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Лимиты": ["create"]}))
):
    await LimitDAO.add(session=db, **body.model_dump())
    db.commit()
    return {"success": True}



@limits_router.get("/limits", response_model=List[Limits])
async def get_limit_list(
        start_date: date,
        finish_date: date,
        is_active: Optional[bool] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Лимиты": ["read"]}))
):
    filters = {k: v for k, v in locals().items() if v is not None and k not in ["db", "current_user"]}
    objs = await LimitDAO.get_by_attributes(session=db, filters=filters)
    return objs



@limits_router.get("/limits/{id}", response_model=Limit)
async def get_limit(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Лимиты": ["read"]}))
):
    obj = await LimitDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return obj



@limits_router.put("/limits", response_model=Limit)
async def update_limit(
        body: UpdateLimit,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Лимиты": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_obj = await LimitDAO.update(session=db, data=body_dict)
    db.commit()
    db.refresh(updated_obj)
    return updated_obj

