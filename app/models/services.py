from pydantic import BaseModel, Field
from typing import Optional


class DictWordModel(BaseModel):
    word: str = Field(str)
    permutation_similarity_index: str = Field(str)


class DictRequestStatsModel(BaseModel):
    process_time_ns: int = Field(int)
    request_path: str = Field(str)


class RequestsStatsResultModel(BaseModel):
    total_requests: int = Field(int)
    avg_processing_time_ns: Optional[float] = Field(float)
