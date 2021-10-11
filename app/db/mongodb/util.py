from confuse import Configuration
from typing import NoReturn

from app.core.logger import LoggerBase
from app.db.mongodb.client import MotorMongoDBUtilClient


class AsyncMongoDBUtils:

    def __init__(self, logger: LoggerBase, db: MotorMongoDBUtilClient, config: Configuration):
        self.logger = logger
        self.db = db
        self.config = config

    async def create_indexes(self, db_name: str) -> NoReturn:
        terms_collection_name = self.config['mongodb']['terms']['collection_name'].get()
        stats_collection_name = self.config['mongodb']['stats']['collection_name'].get()

        self.logger.info('Starting to create indexes for collections')
        await self.db.create_index(db_name,
                                   terms_collection_name,
                                   'permutation_similarity_index', False)
        self.logger.info(f'Finished to index {terms_collection_name} collection')

        await self.db.create_index(db_name,
                                   stats_collection_name,
                                   'request_path', False)
        self.logger.info(f'Finished to index {stats_collection_name} collection')
