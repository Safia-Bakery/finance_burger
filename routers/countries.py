from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import CountryDAO
from schemas.countries import CreateCountry, Country, Countries, UpdateCountry
from utils.utils import PermissionChecker



countries_router = APIRouter()




@countries_router.post("/countries")
async def create_country(
        body: CreateCountry,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Страны": ["create"]}))
):
    await CountryDAO.add(session=db, **body.model_dump(exclude_unset=True))
    db.commit()
    return {"success": True}



@countries_router.get("/countries", response_model=List[Countries])
async def get_country_list(
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Страны": ["read"]}))
):
    filters = {k: v for k, v in locals().items() if v is not None and k not in ["db", "current_user"]}
    objs = await CountryDAO.get_by_attributes(session=db, filters=filters)
    return objs



@countries_router.get("/countries/{id}", response_model=Country)
async def get_country(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Страны": ["read"]}))
):
    obj = await CountryDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return obj



@countries_router.put("/countries", response_model=Country)
async def update_country(
        body: UpdateCountry,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Страны": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_obj = await CountryDAO.update(session=db, data=body_dict)
    db.commit()
    db.refresh(updated_obj)
    return updated_obj

