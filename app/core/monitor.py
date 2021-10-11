import asyncio
import functools
import time

from app.models.exceptions import DBError
from app.services.stats import StatsService
from app.core.containers import container


def monitor_request_duration(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request_path = kwargs['request'].scope['path']
        start_time = time.time_ns()
        response = await func(*args, **kwargs)
        process_time = time.time_ns() - start_time
        is_metric_saved = asyncio.create_task(container[StatsService].try_save_metric(request_path, process_time))
        if not is_metric_saved:
            raise DBError('Failed to save metric')
        return response

    return wrapper
