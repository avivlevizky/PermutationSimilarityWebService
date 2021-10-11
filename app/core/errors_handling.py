import functools
from typing import Callable, Any

from app.core.containers import container
from app.core.logger import LoggerBase
from app.models.exceptions import InternalServerError


def async_request_error_handler(func: Callable) -> Any:

    """
    Error handling decorator for async request functions

    :param func: function which handle errors
    :return: The func returns value
    :exception InternalServerError: Throwing an internal server error
    """
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


def async_func_error_handler_logging(func: Callable) -> Any:

    """
    Decorator error handling by logging the exception from the given func

    :param func: function which handle errors
    :return: The func returns value
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            container[LoggerBase].error(type(e), str(e))
    return wrapper
