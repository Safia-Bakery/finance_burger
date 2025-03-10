from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base_model import TunedModel
from schemas.users import GetUsers


class Log(TunedModel):
    id: UUID
    status: int
    user: Optional[GetUsers]
    created_at: Optional[datetime]



class CreateLog(TunedModel):
    status: int
    request_id: UUID
    user_id: UUID
