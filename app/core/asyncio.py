import asyncio
from abc import ABC, abstractmethod
from asyncio import Future
from typing import Any


class EventLoopBase(ABC):

    @abstractmethod
    def get_loop(self):
        """
        Getting the current event loop
        """
        ...

    @abstractmethod
    def run(self, future: Future) -> Any:
        """
        Execute the given future in the event loop

        :param future: The future which the event loop will resolve
        :return: Result of the resolved given future
        """
        ...


class AsyncIOEventLoop(EventLoopBase):
    def __init__(self):
        """
        EventLoopBase implementation backed by the native asyncio lib
        """
        self._loop = asyncio.get_event_loop()

    def get_loop(self):
        return self._loop

    def run(self, future) -> Any:
        return self._loop.run_until_complete(future)




