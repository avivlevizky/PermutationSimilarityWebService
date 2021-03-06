
from confuse import Configuration
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.error_handlers import request_validation_exception_handler, internal_exception_handler
from app.api.routers import default_router, dict_router
from app.core.containers import container

from app.models.exceptions import InternalServerError


def get_app() -> FastAPI:
    """
    Initialize the FastAPI application with all relevant settings
    :return: FastAPI application
    """
    project_name = container[Configuration]['app']['project_name'].get()
    app = FastAPI(title=project_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(default_router)
    app.include_router(dict_router)

    app.exception_handler(RequestValidationError)(request_validation_exception_handler)
    app.exception_handler(InternalServerError)(internal_exception_handler)

    return app


fastapi_app = get_app()
