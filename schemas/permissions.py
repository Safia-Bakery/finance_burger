from uuid import UUID

from schemas.base_model import TunedModel



class GetPermission(TunedModel):
    id: UUID
    name: str
    action: str
