from fastapi.encoders import jsonable_encoder
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.core.containers import container
from app.core.logger import LoggerBase
from app.models.exceptions import InternalServerError


def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    container[LoggerBase].error()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


def internal_exception_handler(request: Request, exc: InternalServerError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"message": "Internal Error", "detail": exc.error}))
