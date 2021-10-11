import sys
from abc import ABC, abstractmethod
from typing import TextIO, Type

from confuse import Configuration
from loguru import logger


class LoggerBase(ABC):

    @staticmethod
    @abstractmethod
    def logger_maker(sinker: TextIO, logger_format: str):
        ...

    @abstractmethod
    def info(self, message: str):
        ...

    @abstractmethod
    def trace(self, message: str):
        ...

    @abstractmethod
    def debug(self, message: str):
        ...

    @abstractmethod
    def error(self, exception: Type[Exception], message: str):
        ...


class LoguruLogger(LoggerBase):

    def __init__(self, config: Configuration):
        logger.remove()
        logger_format = config["app"]["logger"]["format"].get()
        self._logger = self.logger_maker(sys.stdout, logger_format)

    @staticmethod
    def logger_maker(sinker: TextIO, logger_format: str):
        logger.add(
            sinker,
            colorize=True,
            enqueue=True,
            backtrace=True,
            format=logger_format
        )
        return logger.bind(request_id=None, method=None)

    def info(self, message: str):
        self._logger.info(message)

    def trace(self, message: str):
        self._logger.trace(message)

    def debug(self, message: str):
        self._logger.debug(message)

    def error(self, exception: Type[Exception], message: str):
        self._logger.exception(f"{exception.__name__}: {message}")
