
from confuse import Configuration

from app.core.logger import LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient
from app.models.services import DictRequestStatsModel, RequestStatsResultModel


class StatsService:
    def __init__(self, logger: LoggerBase, db_client: AsyncMongoDBBaseClient, config: Configuration):
        self.logger = logger
        self.db_name = config["mongodb"]["db_name"]
        self.db_collection_name = config["mongodb"]["stats"]["collection_name"]
        self.db_client = db_client

    async def try_save_metric(self, request_path: str, process_time: float) -> bool:
        req_stats = DictRequestStatsModel(process_time_ns=process_time, request_path=request_path)
        return await self.db_client.try_to_insert(self.db_name, self.db_collection_name, req_stats.dict())

    async def get_terms_requests_stats(self) -> RequestStatsResultModel:
        pipeline_stats = [
            {'$match': {'request_path': "/api/v1/similar"}},
            {'$group': {'_id': 0, 'count': {'$sum': 1}, 'avg_process_time': {'$avg': "$process_time_ns"}}},
        ]

        results_stats = await self.db_client.aggregate(self.db_name, self.db_collection_name, pipeline_stats)
        total_requests = results_stats[0]['count']
        avg_processing_time_ns = results_stats[0]['avg_process_time']
        return RequestStatsResultModel(total_requests=total_requests, avg_processing_time_ns=avg_processing_time_ns)
