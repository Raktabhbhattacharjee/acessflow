from fastapi import APIRouter
from app.core.config import settings
from app.core.responses import success_response

router = APIRouter()


@router.get("/health")
async def health():
    return success_response({"service": settings.app_name, "status": "ok"})
