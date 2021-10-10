import asyncio
from abc import ABC, abstractmethod
from typing import Any


class EventLoopBase(ABC):

    @abstractmethod
    def get_loop(self):
        ...

    @abstractmethod
    def run(self, future):
        ...


class AsyncIOEventLoop(EventLoopBase):

    def __init__(self):
        self._loop = asyncio.get_event_loop()

    def get_loop(self):
        return self._loop

    def run(self, future) -> Any:
        return self._loop.run_until_complete(future)
