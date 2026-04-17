from fastapi import FastAPI, Request
from app.routes.upload import router as upload_router
from app.routes.health import router as health_router
from app.core.logger import get_logger
from app.core.exceptions import AppException
from app.core.middleware import RequestLoggingMiddleware
from fastapi.responses import JSONResponse
from app.core.lifespan import lifespan
from app.core.responses import error_response

logger = get_logger("main")

app = FastAPI(
    title="AcessFlow",
    description="Learning backend system for deployment and system behavior",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"Handled AppException: {exc.message}")
    return JSONResponse(status_code=400, content=error_response(exc.message))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch any unexpected exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500, content=error_response("Internal server error")
    )


app.include_router(upload_router)
app.include_router(health_router)

logger.info("Application started")
