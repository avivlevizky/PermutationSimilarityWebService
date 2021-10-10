from typing import Sequence

from pydantic import BaseModel


class SimilarResponse(BaseModel):
    similar: Sequence[str]


class StatsResponse(BaseModel):
    totalWords: int
    totalRequests: int
    avgProcessingTimeNs: float
