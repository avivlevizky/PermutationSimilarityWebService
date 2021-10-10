from typing import Dict

from pydantic import BaseModel, Field
from fastapi import Request


class ClientErrorModel(BaseModel):
    error_info: str = Field(str)


class ServerErrorModel(BaseModel):
    request_cookies: Dict = Field(Dict)


class RequestValidationError(Exception):
    def __init__(self, error_info: str):
        self.error = ClientErrorModel(error_info=error_info)


class InternalServerError(Exception):
    def __init__(self, request: Request):
        self.error = ServerErrorModel(request_cookies=request.cookies)


class DBError(Exception):
    def __init__(self, message):
        self.error = message
