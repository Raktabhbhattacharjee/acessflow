from fastapi import APIRouter, UploadFile, File
from app.services.file_service import handle_upload

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    print(f"Upload endpoint called: {file.filename}")

    if not file.filename:
        return {"status": "error", "message": "Invalid file"}

    file_bytes = await file.read()

    path = handle_upload(file_bytes, file.filename)

    return {
        "status": "success",
        "file_path": path
    }