import logging
import datetime

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.requests import Request

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        logger.log(
            level=logging.INFO,
            msg=f"[{datetime.datetime.now()}] [{request.client.host}] --> {request.method} {request.url.path}" #type: ignore
        )

        response = await call_next(request)

        logger.log(
            level=logging.INFO,
            msg=f"[{datetime.datetime.now()}] [{request.client.host}] <-- {request.method} {request.url.path} {response.status_code}" #type: ignore
        )
        return response
