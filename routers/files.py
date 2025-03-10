import os
from datetime import datetime
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
        files: List[UploadFile] = File(...),
        # db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions={"Files": ["read"]}))
):
    base_dir = "files"
    date_dir = datetime.now().strftime("%Y/%m/%d")  # Create a path like "2025/03/10"
    save_dir = os.path.join(base_dir, date_dir)

    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

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

    return {"file_paths": file_paths}
