from fastapi.encoders import jsonable_encoder
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.core.containers import container
from app.core.logger import LoggerBase
from app.models.exceptions import InternalServerError


def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """
    handler for request validation exception

    :param _: FastAPI request
    :param exc: FastAPI exception which represents the validation exception
    :return: The client error message with matched details for the given request
    """
    container[LoggerBase].error()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


def internal_exception_handler(_: Request, exc: InternalServerError) -> JSONResponse:
    """
    handler for request validation exception

    :param _: FastAPI request
    :param exc: Custom exception which represents the server exception
    :return: The internal server error message with matched details for the given request
    """
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"message": "Internal Error", "detail": exc.error}))
