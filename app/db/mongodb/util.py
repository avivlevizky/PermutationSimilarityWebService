from confuse import Configuration

from app.core.logger import LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient


class AsyncMongoDBUtil:

    def __init__(self, logger: LoggerBase, db: AsyncMongoDBBaseClient, config: Configuration):
        self.logger = logger
        self.db = db
        self.config = config

    async def create_indexes(self):
        db_name = self.config['mongodb']['db_name']
        terms_collection_name = self.config['mongodb']['terms']['collection_name']
        stats_collection_name = self.config['mongodb']['stats']['collection_name']

        self.logger.info('Starting to create indexes for collections')
        await self.db.create_index(db_name,
                                   terms_collection_name,
                                   'permutation_similarity_index', False)
        self.logger.info(f'Finished to index {terms_collection_name} collection')

        await self.db.create_index(db_name,
                                   stats_collection_name,
                                   'request_path', False)
        self.logger.info(f'Finished to index {stats_collection_name} collection')
