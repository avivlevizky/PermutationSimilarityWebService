from confuse import Configuration
from typing import NoReturn

from app.core.logger import LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseUtilClient


class AsyncMongoDBUtils:

    def __init__(self, logger: LoggerBase, db: AsyncMongoDBBaseUtilClient, config: Configuration):
        self.logger = logger
        self.db = db
        self.config = config

    async def create_indexes(self, db_name: str) -> NoReturn:
        """
        Index words and stats collections
        :param db_name: The database name which the collections indexing taking place
        """
        words_collection_name = self.config['mongodb']['words']['collection_name'].get()
        stats_collection_name = self.config['mongodb']['stats']['collection_name'].get()

        self.logger.info('Starting to create indexes for collections')
        await self.db.create_index(db_name,
                                   words_collection_name,
                                   'permutation_similarity_index', False)
        self.logger.info(f'Finished to index {words_collection_name} collection')

        await self.db.create_index(db_name,
                                   stats_collection_name,
                                   'request_path', False)
        self.logger.info(f'Finished to index {stats_collection_name} collection')
