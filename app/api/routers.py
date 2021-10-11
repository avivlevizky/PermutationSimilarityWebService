from confuse import Configuration
from fastapi import APIRouter, Request

from app.core.errors_handling import async_request_error_handler
from app.models.responses import SimilarResponse, StatsResponse
from app.core.containers import container
from app.core.monitor import monitor_request_duration
from app.services.analytics import AnalyticsService
from app.services.words import WordsService


app_router = APIRouter(
    prefix=container[Configuration]["app"]["api_router"]["prefix"].get(),
)


# TODO: can be cacheable(LRU)
@app_router.get("/similar", response_model=SimilarResponse)
@async_request_error_handler
@monitor_request_duration
async def similar(word: str, request: Request) -> SimilarResponse:
    """
    Controller handler for the similar API

    :param word: The word to search after match similar words in the given dictionary
    :param request: The given FastAPI request
    :return: List of the similar words
    """
    words_results = await container[WordsService].find_similar_words(word)
    return SimilarResponse(similar=words_results)


@app_router.get("/stats", response_model=StatsResponse)
@async_request_error_handler
@async_request_error_handler
async def stats(request: Request) -> StatsResponse:
    """
    Controller handler for the stats API

    :param request: The given FastAPI request
    :return: Stats of the words requests
    """
    total_words = await container[WordsService].count_all_words()
    words_requests_stats = await container[AnalyticsService].get_similar_requests_stats()
    total_requests = words_requests_stats.total_requests
    avg_processing_time_ns = words_requests_stats.avg_processing_time_ns
    return StatsResponse(totalWords=total_words,
                         totalRequests=total_requests,
                         avgProcessingTimeNs=avg_processing_time_ns)
