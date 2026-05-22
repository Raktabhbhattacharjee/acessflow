from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies import get_storage
from app.storage.base import StorageBackend
from app.validators.file_validator import validate_file
from app.core.logger import get_logger
from app.core.responses import success_response
from app.core.config import settings

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
    size_bytes = len(file_bytes)
    content_type = file.content_type
    storage_reference = await storage.save(file_bytes, file.filename)

    logger.info(f"Upload successful: {file.filename} → {storage_reference}")

    return success_response(
        {
            "filename": file.filename,
            "storage_backend": settings.storage_backend,
            "storage_reference": storage_reference,
            "size_bytes": size_bytes,
            "content_type": content_type,
        }
    )
