from fastapi import FastAPI, Request
from app.routes.upload import router as upload_router
from app.routes.health import router as health_router
from app.core.logger import get_logger
from app.core.exceptions import AppException
from app.core.middleware import RequestLoggingMiddleware
from fastapi.responses import JSONResponse
from app.core.lifespan import lifespan

logger = get_logger("main")

app = FastAPI(
    title="AcessFlow",
    description="Learning backend system for deployment and system behavior",
    version="0.1.0",
    lifespan=lifespan
)
app.add_middleware(RequestLoggingMiddleware)


# ✅ Global Exception Handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"Handled AppException: {exc.message}")

    return JSONResponse(
        status_code=400, content={"status": "error", "message": exc.message}
    )


app.include_router(upload_router)
app.include_router(health_router)

logger.info("Application started")
