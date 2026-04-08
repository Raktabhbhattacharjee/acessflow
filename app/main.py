from fastapi import FastAPI
from datetime import datetime, timezone

from app.routes import upload

app = FastAPI()


@app.get("/")
def health_check():
    print("Health check endpoint called")

    return {
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


app.include_router(upload.router)