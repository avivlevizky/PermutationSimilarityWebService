import functools

from app.core.containers import container
from app.core.logger import LoggerBase
from app.models.exceptions import InternalServerError


def async_request_error_handler(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            container[LoggerBase].error(type(e), str(e))
            raise InternalServerError(request)
    return wrapper


def async_func_error_handler(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            container[LoggerBase].error(type(e), str(e))
    return wrapper
