from confuse import Configuration
from fastapi import APIRouter, Request

from app.core.errors_handling import async_request_error_handler
from app.models.responses import SimilarResponse, StatsResponse
from app.core.containers import container
from app.core.monitor import monitor_request_duration
from app.services.stats import StatsService
from app.services.terms import TermsService


app_router = APIRouter(
    prefix=container[Configuration]["app"]["api_router"]["prefix"],
)


terms_service: TermsService = container[TermsService]
stats_service: StatsService = container[StatsService]


@app_router.get("/similar", response_model=SimilarResponse)
@async_request_error_handler
@monitor_request_duration(stats_service)
async def similar(word: str, request: Request):
    terms_results = await terms_service.find_similar_term(word)
    return SimilarResponse(similar=terms_results)


@app_router.get("/stats", response_model=StatsResponse)
@async_request_error_handler
@async_request_error_handler
async def stats(request: Request):
    total_words = await terms_service.count_all_terms()
    terms_requests_stats = await stats_service.get_terms_requests_stats()
    total_requests, avg_processing_time_ns = terms_requests_stats.total_requests, terms_requests_stats.avg_processing_time_ns
    return StatsResponse(totalWords=total_words,
                         totalRequests=total_requests,
                         avgProcessingTimeNs=avg_processing_time_ns)
