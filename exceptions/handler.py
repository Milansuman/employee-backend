from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from exceptions.exceptions import AppException, NotFoundException, ConflictException, BadRequestException

STATUS_MAP: dict[type[AppException], int] = {
    NotFoundException: status.HTTP_404_NOT_FOUND,
    ConflictException: status.HTTP_409_CONFLICT,
    BadRequestException: status.HTTP_400_BAD_REQUEST,
}

def configure_error_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def not_found_handler(request: Request, exception: AppException):
        return JSONResponse(
            status_code=STATUS_MAP[type(exception)],
            content={
                "detail": str(exception)
            }
        )
