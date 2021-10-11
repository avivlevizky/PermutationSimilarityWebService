
from confuse import Configuration

from app.core.logger import LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient
from app.models.services import DictRequestStatsModel, RequestsStatsResultModel


class AnalyticsService:
    def __init__(self, logger: LoggerBase, db_client: AsyncMongoDBBaseClient, config: Configuration):
        self._logger = logger
        self._db_name = config["mongodb"]["db_name"].get()
        self._db_collection_name = config["mongodb"]["stats"]["collection_name"].get()
        self._db_client = db_client

    async def try_save_metric(self, request_path: str, process_time: float) -> bool:
        """
        Try to save the stats metric of the given requests path (request_path)

        :param request_path: Request path which the metric is belongs to
        :param process_time: Process time value
        :return: Represent if the metric is successfully saved
        """
        req_stats = DictRequestStatsModel(process_time_ns=process_time, request_path=request_path)
        self._logger.trace(f"Stats process time metric: {str(req_stats)}")

        return await self._db_client.try_to_insert(self._db_name, self._db_collection_name, req_stats.dict())

    async def get_similar_requests_stats(self) -> RequestsStatsResultModel:
        """
        Get the similar api request's stats metric data

        :return: The RequestsStatsResultModel model
        """
        pipeline = [
            {'$match': {'request_path': "/api/v1/similar"}},
            {'$group': {'_id': 0, 'count': {'$sum': 1}, 'avg_process_time': {'$avg': "$process_time_ns"}}},
        ]

        results_stats = await self._db_client.aggregate(self._db_name, self._db_collection_name, pipeline)
        if results_stats:
            total_requests = results_stats[0]['count']
            avg_processing_time_ns = results_stats[0]['avg_process_time']
        else:
            total_requests = 0
            avg_processing_time_ns = None
        return RequestsStatsResultModel(total_requests=total_requests, avg_processing_time_ns=avg_processing_time_ns)
