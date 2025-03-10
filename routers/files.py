from typing import List, Optional

from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.ext.asyncio import AsyncSession

from core.session import get_db
from dal.dao import InvoiceDAO, ContractDAO, FileDAO
from schemas.files import CreateFile, GetFile
from utils.utils import PermissionChecker



files_router = APIRouter()


@files_router.post("/files/upload", response_model=GetFile)
async def upload_files(
        # body: CreateFile,
        files: List[UploadFile] = File(...),
        # db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Files": ["read"]}))
):
    # invoice = None
    # contract = None
    # if body.invoice is not None:
    #     invoice = await InvoiceDAO.add(session=db, **{"request_id": body.request_id})
    # if body.contract is not None:
    #     contract = await ContractDAO.add(session=db, **{"request_id": body.request_id})

    file_paths = []
    for file in files:
        file_path = f"files/{file.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file_paths.append(file_path)

    # file = await FileDAO.add(
    #     session=db,
    #     **{
    #         "file_path": file_paths,
    #         "contract_id": contract.id if contract is not None else None,
    #         "invoice_id": invoice.id if invoice is not None else None
    #     }
    # )

    return {"file_paths": file_paths}
    # return file
