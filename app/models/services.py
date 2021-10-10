from pydantic import BaseModel, Field


class DictTermModel(BaseModel):
    term: str = Field(str)
    permutation_similarity_index: str = Field(str)


class DictRequestStatsModel(BaseModel):
    process_time_ns: int = Field(int)
    request_path: str = Field(str)


class RequestStatsResultModel(BaseModel):
    total_requests: int = Field(int)
    avg_processing_time_ns: int = Field(int)
