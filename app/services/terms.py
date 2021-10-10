from typing import Sequence, List

from confuse import Configuration
from fastapi import Path

from app.core.logger import LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient
from app.models.exceptions import DBError
from app.models.services import DictTermModel


class TermsService:
    def __init__(self, logger: LoggerBase, db_client: AsyncMongoDBBaseClient, config: Configuration):
        self.logger = logger
        self.db_name = config["mongodb"]["db_name"]
        self.db_collection_name = config["mongodb"]["terms"]["collection_name"]
        self.db_client = db_client

    async def _try_insert_terms(self, dict_terms: Sequence[DictTermModel]):
        docs = [term.dict() for term in dict_terms]
        return await self.db_client.try_insert_many(self.db_name, self.db_collection_name, docs)

    # TODO: possible to stream the list
    async def find_similar_term(self, term: str, length_limit=100) -> List[str]:
        sorted_term = "".join(sorted(term))
        query = {'permutation_similarity_index': sorted_term}
        return [doc['term']
                async for doc in self.db_client.find(self.db_name, self.db_collection_name, query, length_limit)]

    async def count_all_terms(self) -> int:
        pipeline_terms = [
            {'$group': {'_id': 0, 'count': {'$sum': 1}}},
        ]
        results_terms = await self.db_client.aggregate(self.db_name, self.db_collection_name, pipeline_terms)
        return results_terms[0]['count']

    async def process_data_from_path_by_chunk(self, data_path: Path, chunk_size: int = 5000) -> int:
        total_terms_inserted = 0
        with data_path.open('r') as f:
            processed_terms = []
            is_end_file = False
            while not is_end_file:
                processed_terms.clear()
                for _ in range(chunk_size):
                    word = f.readline().strip()
                    if not word:
                        is_end_file = True
                        break
                    sorted_word = "".join(sorted(word))
                    dict_term = DictTermModel(term=word, permutation_similarity_index=sorted_word)
                    processed_terms.append(dict_term)
                if processed_terms:
                    total_terms_inserted += len(processed_terms)
                    is_terms_inserted = await self._try_insert_terms(processed_terms)
                    if not is_terms_inserted:
                        raise DBError('Failed to save many terms docs')
        return total_terms_inserted
