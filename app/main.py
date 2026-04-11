from fastapi import FastAPI, Request
from datetime import datetime, timezone

from app.routes.upload import router as upload_router
from app.core.logger import get_logger
from app.core.exceptions import AppException
from fastapi.responses import JSONResponse

logger = get_logger("main")

app = FastAPI(
    title="AcessFlow",
    description="Learning backend system for deployment and system behavior",
    version="0.1.0"
)


# ✅ Global Exception Handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"Handled AppException: {exc.message}")

    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": exc.message
        }
    )


@app.get("/")
def health_check():
    logger.info("Health check endpoint called")

    return {
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


app.include_router(upload_router)

logger.info("Application started")