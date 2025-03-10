from datetime import datetime
from typing import Optional
from uuid import UUID

from schemas.base_model import TunedModel
from schemas.files import GetFile



class Contract(TunedModel):
    id: UUID
    request_id: UUID
    file: Optional[GetFile]
    created_at: Optional[datetime]



class CreateContract(TunedModel):
    request_id: UUID


