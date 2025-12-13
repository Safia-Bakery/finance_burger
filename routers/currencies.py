from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import CurrencyDAO
from schemas.currencies import Currency, CreateCurrency, Currencies, UpdateCurrency
from utils.utils import PermissionChecker



currencies_router = APIRouter()



@currencies_router.post("/currencies", response_model=Currency)
async def create_currency(
        body: CreateCurrency,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Валюты": ["create"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    body_dict["name"] = body_dict.get("name").strip() if body_dict.get("name") else ""
    created_currency = await CurrencyDAO.add(session=db, **body_dict)
    db.commit()
    return created_currency


@currencies_router.get("/currencies", response_model=List[Currencies])
async def get_currency_list(
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Валюты": ["read_list"]}))
):
    filters = {k: v for k, v in locals().items() if v is not None and k not in ["db", "current_user"]}

    query = await CurrencyDAO.get_all(session=db, filters=filters if filters else None)
    currencies = db.execute(query).scalars().all()
    return currencies


@currencies_router.get("/currencies/{id}", response_model=Currency)
async def get_currency(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Валюты": ["read_detail"]}))
):
    currency = await CurrencyDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    if currency is None:
        raise HTTPException(status_code=400, detail="Валюта не найдена !")

    return currency


@currencies_router.put("/currencies", response_model=Currency)
async def update_currency(
        body: UpdateCurrency,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Валюты": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_currency = await CurrencyDAO.update(session=db, data=body_dict)
    db.commit()
    db.refresh(updated_currency)
    return updated_currency


@currencies_router.delete("/currencies")
async def delete_currency(
        id: Optional[UUID],
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Валюты": ["delete"]}))
):
    deleted_currency = await CurrencyDAO.delete(session=db, filters={"id": id})
    if deleted_currency is True:
        return {"Message": "Валюта удалена успешно !"}
    else:
        raise HTTPException(status_code=400, detail="Произошла ошибка !")
