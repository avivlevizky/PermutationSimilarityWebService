from typing import Sequence, Optional

from pydantic import BaseModel


class SimilarResponse(BaseModel):
    similar: Sequence[str]


class StatsResponse(BaseModel):
    totalWords: int
    totalRequests: int
    avgProcessingTimeNs: Optional[float]
