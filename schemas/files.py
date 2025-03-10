from datetime import datetime
from typing import Optional, List
from uuid import UUID

from schemas.base_model import TunedModel



class GetFile(TunedModel):
    id: UUID
    file_paths: List[str]
    contract_id: Optional[UUID] = None
    invoice_id: Optional[UUID] = None
    created_at: Optional[datetime]


class CreateFile(TunedModel):
    request_id: UUID
    contract: Optional[bool] = None
    invoice: Optional[bool] = None
    # file_path: str
    # contract_id: Optional[UUID] = None
    # invoice_id: Optional[UUID] = None


