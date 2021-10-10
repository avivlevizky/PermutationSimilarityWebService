
from confuse import Configuration
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.error_handlers import request_validation_exception_handler, internal_exception_handler
from app.api.routers import app_router
from app.core.containers import container

from app.core.logger import LoguruLogger
from app.models.exceptions import InternalServerError


def get_app():
    config = container[Configuration]
    project_name = config['app']['project_name']
    app = FastAPI(title=project_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.logger = container[LoguruLogger]

    app.include_router(app_router)

    app.exception_handler(RequestValidationError)(request_validation_exception_handler)
    app.exception_handler(InternalServerError)(internal_exception_handler)

    return app


fastapi_app = get_app()
