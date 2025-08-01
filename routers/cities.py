from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import CityDAO, LimitDAO
from schemas.cities import CreateCity, City, Cities, UpdateCity
from utils.utils import PermissionChecker



cities_router = APIRouter()




@cities_router.post("/cities")
async def create_city(
        body: CreateCity,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Города": ["create"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    body_dict.pop("limit")
    created_city = await CityDAO.add(session=db, **body_dict)
    if created_city is not None:
        await LimitDAO.add(
            session=db,
            **{
                "city_id": created_city.id,
                "value": body.limit
            }
        )

    db.commit()
    return {"success": True}



@cities_router.get("/cities", response_model=List[Cities])
async def get_city_list(
        country_id: Optional[str] = None,
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Города": ["read"]}))
):
    filters = {k: v for k, v in locals().items() if v is not None and k not in ["db", "current_user"]}
    objs = await CityDAO.get_by_attributes(session=db, filters=filters)
    return objs



@cities_router.get("/cities/{id}", response_model=City)
async def get_city(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Города": ["read"]}))
):
    city = await CityDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    limit = await LimitDAO.get_by_attributes(session=db, filters={"city_id": city.id}, first=True)
    if limit is not None:
        city.limit = limit.value
    return city



@cities_router.put("/cities", response_model=City)
async def update_city(
        body: UpdateCity,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Города": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    body_dict.pop("limit")
    updated_city = await CityDAO.update(session=db, data=body_dict)
    limit_obj = await LimitDAO.get_by_attributes(session=db, filters={"city_id": updated_city.id}, first=True)
    if limit_obj is not None and body.limit is not None:
        await LimitDAO.update(session=db, data={"id": limit_obj.id, "value": body.limit})
    db.commit()
    db.refresh(updated_city)
    return updated_city

