from fastapi import FastAPI
from datetime import datetime, timezone

from app.routes.upload import router as upload_router

app = FastAPI(
    title="AcessFlow",
    description="Learning backend system for deployment and system behavior",
    version="0.1.0"
)


@app.get("/")
def health_check():
    print("Health check endpoint called")

    return {
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Include routes
app.include_router(upload_router)