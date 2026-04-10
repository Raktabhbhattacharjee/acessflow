from fastapi import APIRouter, UploadFile, File
from app.services.file_service import handle_upload
from app.core.logger import get_logger
router = APIRouter(prefix="/upload", tags=["upload"])
logger = get_logger("upload_route")

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    logger.info(f"Upload request received: {file.filename}")

    if not file.filename:
        return {"status": "error", "message": "Invalid file"}

    file_bytes = await file.read()

    path = handle_upload(file_bytes, file.filename)
    logger.info(f"Upload successful: {file.filename} → {path}")
    return {
        "status": "success",
        "file_path": path
    }