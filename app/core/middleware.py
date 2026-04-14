import time
import uuid
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.logger import get_logger

logger = get_logger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info(
            {
                "event": "request_started",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            }
        )

        response = await call_next(request)

        latency = round((time.time() - start_time) * 1000, 2)

        logger.info(
            {
                "event": "request_finished",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": latency,
            }
        )

        response.headers["X-Request-ID"] = request_id
        return response
