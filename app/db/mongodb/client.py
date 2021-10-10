from typing import Sequence, Any, List, AsyncGenerator, NoReturn
from abc import ABC, abstractmethod
import motor.motor_asyncio
from confuse import Configuration

from app.core.asyncio import EventLoopBase
from app.core.logger import LoggerBase


class AsyncMongoDBBaseClient(ABC):

    @abstractmethod
    async def try_to_insert(self, db_name: str, collection_name: str, doc: dict) -> bool:
        ...

    @abstractmethod
    async def try_insert_many(self, db_name: str, collection_name: str, docs: Sequence[dict]) -> bool:
        ...

    @abstractmethod
    async def find(self, db_name: str, collection_name: str, doc: dict, length_limit=100) -> AsyncGenerator:
        ...

    @abstractmethod
    async def create_index(self, db_name: str, collection_name: str, field: str, unique: bool = False) -> str:
        ...

    @abstractmethod
    async def aggregate(self, db_name: str, collection_name: str, pipeline: List[dict[Any, Any]]) -> dict:
        ...

    @abstractmethod
    def close(self) -> NoReturn:
        ...


class MotorMongoDBClient(AsyncMongoDBBaseClient):
    def __init__(self,
                 logger: LoggerBase,
                 config: Configuration,
                 event_loop: EventLoopBase):
        self._logger = logger
        db_url = config['mongodb']['url']
        max_connections_count = config['mongodb']['max_connections_count']
        min_connections_count = config['mongodb']['min_connections_count']
        server_selection_timeout_ms = config['mongodb']['server_selection_timeout_ms']
        self._mongo_client = motor.motor_asyncio.AsyncIOMotorClient(db_url,
                                                                    serverSelectionTimeoutMS=server_selection_timeout_ms,
                                                                    maxPoolSize=max_connections_count,
                                                                    minPoolSize=min_connections_count,
                                                                    io_loop=event_loop.get_loop())

    async def try_to_insert(self, db_name: str, collection_name: str, doc: dict) -> bool:
        result = await self._mongo_client[db_name][collection_name].insert_one(doc)
        return result.acknowledged

    async def try_insert_many(self, db_name: str, collection_name: str, docs: Sequence[dict]) -> bool:
        result = await self._mongo_client[db_name][collection_name].insert_many(docs)
        return result.acknowledged

    async def find(self, db_name: str, collection_name: str, doc: dict, length_limit=100) -> AsyncGenerator:
        cursor = self._mongo_client[db_name][collection_name].find(doc)
        for document in await cursor.to_list(length=length_limit):
            yield document

    async def create_index(self, db_name: str, collection_name: str, field: str, unique: bool = False) -> str:
        return await self._mongo_client[db_name][collection_name].create_index(field, unique=unique)

    async def aggregate(self, db_name: str, collection_name: str, pipeline: dict) -> dict:
        return await self._mongo_client[db_name][collection_name].aggregate(pipeline).to_list(1)

    def close(self) -> NoReturn:
        self._mongo_client.close()
