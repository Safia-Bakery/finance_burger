from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core.session import get_db
from dal.dao import PermissionDAO
from schemas.permissions import GetPermission
from utils.utils import PermissionChecker



permissions_router = APIRouter()




@permissions_router.get("/permissions", response_model=List[GetPermission])
async def get_permission_list(
        permission_group: Optional[UUID] = None,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Permissions": ["read"]}))
):
    filters = {}
    if permission_group is not None:
        filters["group_id"] = permission_group

    permissions = await PermissionDAO.get_by_attributes(session=db, filters=filters if filters else None)
    return permissions

