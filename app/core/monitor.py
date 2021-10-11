import asyncio
import functools
import time
from typing import Callable, Any

from app.models.exceptions import DBError
from app.services.analytics import AnalyticsService
from app.core.containers import container


def monitor_request_duration(func: Callable) -> Any:
    """
    Decorator monitor the requests functions by measuring the process time (nano seconds) of the given func
    and insert it as a metric in the database

    :param func: function which handle errors
    :return: The func returns value
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request_path = kwargs['request'].scope['path']
        start_time = time.time_ns()
        response = await func(*args, **kwargs)
        process_time = time.time_ns() - start_time
        is_metric_saved = asyncio.create_task(container[AnalyticsService].try_save_metric(request_path, process_time))
        if not is_metric_saved:
            raise DBError('Failed to save metric')
        return response

    return wrapper
