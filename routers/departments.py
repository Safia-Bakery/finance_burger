from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.session import get_db
from dal.dao import DepartmentDAO
from schemas.departments import Department, CreateDepartment, Departments, UpdateDepartment
from utils.utils import PermissionChecker

departments_router = APIRouter()



@departments_router.post("/departments", response_model=Department)
async def create_department(
        body: CreateDepartment,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Departments": ["create"]}))
):
    created_department = await DepartmentDAO.add(session=db, **body.model_dump())
    db.commit()
    db.refresh(created_department)
    return created_department


@departments_router.get("/departments", response_model=Page[Departments])
async def get_department_list(
        name: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Departments": ["read"]}))
):
    filters = {}
    if name is not None:
        filters["name"] = name

    departments = await DepartmentDAO.get_by_attributes(session=db, filters=filters if filters else None)
    return paginate(departments)


@departments_router.get("/departments/{id}", response_model=Department)
async def get_department(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Departments": ["read"]}))
):
    department = await DepartmentDAO.get_by_attributes(session=db, filters={"id": id}, first=True)
    return department


@departments_router.put("/departments", response_model=Department)
async def update_department(
        body: UpdateDepartment,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Departments": ["update"]}))
):
    body_dict = body.model_dump(exclude_unset=True)
    updated_department = await DepartmentDAO.update(session=db, data=body_dict)
    db.commit()
    db.refresh(updated_department)
    return updated_department


@departments_router.delete("/departments", response_model=List[Departments])
async def delete_department(
        id: Optional[UUID],
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Departments": ["delete"]}))
):
    deleted_departments = await DepartmentDAO.delete(session=db, filters={"id": id})
    db.commit()
    return deleted_departments

