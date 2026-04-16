from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies import get_storage
from app.storage.base import StorageBackend
from app.validators.file_validator import validate_file
from app.core.logger import get_logger

router = APIRouter(prefix="/upload", tags=["upload"])
logger = get_logger("upload_route")


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    storage: StorageBackend = Depends(get_storage),
):
    logger.info(f"Upload request received: {file.filename}")

    validate_file(file)

    file_bytes = await file.read()
    path = await storage.save(file_bytes, file.filename)

    logger.info(f"Upload successful: {file.filename} → {path}")

    return {"status": "success", "file_path": path}
