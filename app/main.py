from fastapi import FastAPI
from datetime import datetime, timezone

from app.routes.upload import router as upload_router
from app.core.logger import get_logger

logger = get_logger("main")

app = FastAPI(
    title="AcessFlow",
    description="Learning backend system for deployment and system behavior",
    version="0.1.0"
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