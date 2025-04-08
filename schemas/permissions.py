from typing import Optional, List
from uuid import UUID

from schemas.base_model import TunedModel



class GetPermission(TunedModel):
    id: UUID
    name: str
    action: str



class GetPermissionGroup(TunedModel):
    id: UUID
    name: str
    is_active: bool
    permissions: Optional[List[GetPermission]] = None

