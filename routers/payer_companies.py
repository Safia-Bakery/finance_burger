from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import PayerCompanyDAO
from schemas.payer_companies import PayerCompany, CreatePayerCompany, PayerCompanies, UpdatePayerCompany
from utils.utils import PermissionChecker



payer_companies_router = APIRouter()



@payer_companies_router.post("/payer-companies", response_model=PayerCompany)
async def create_company(
        body: CreatePayerCompany,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Компании-плательщики": ["create"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    body_dict["name"] = body_dict.get("name").strip() if body_dict.get("name") else ""
    created_company = await PayerCompanyDAO.add(session=db, **body_dict)
    db.commit()
    return created_company


@payer_companies_router.get("/payer-companies", response_model=Page[PayerCompanies])
async def get_company_list(
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions={"Компании-плательщики": ["read"]}))
):
    filters = {k: v for k, v in locals().items() if v is not None and k not in ["db", "current_user"]}

    query = await PayerCompanyDAO.get_all(session=db, filters=filters if filters else None)
    companies = db.execute(query).scalars().all()

    return paginate(companies)


@payer_companies_router.get("/payer-companies/{id}", response_model=PayerCompany)
async def get_company(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions={"Компании-плательщики": ["read"]}))
):
    company = await PayerCompanyDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    if company is None:
        raise HTTPException(status_code=400, detail="Компания-плательщик не найден!")

    return company


@payer_companies_router.put("/payer-companies", response_model=PayerCompany)
async def update_company(
        body: UpdatePayerCompany,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Компании-плательщики": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_company = await PayerCompanyDAO.update(session=db, data=body_dict)
    db.commit()
    db.refresh(updated_company)
    return updated_company


@payer_companies_router.delete("/payer-companies")
async def delete_company(
        id: Optional[UUID],
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Компании-плательщики": ["delete"]}))
):
    deleted_company = await PayerCompanyDAO.delete(session=db, filters={"id": id})
    if deleted_company is True:
        return {"Message": "Компания-плательщик удалена успешно !"}
    else:
        raise HTTPException(status_code=400, detail="Произошла ошибка !")
