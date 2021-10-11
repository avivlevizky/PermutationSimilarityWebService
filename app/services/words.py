from typing import List, NoReturn

from confuse import Configuration
from fastapi import Path

from app.core.logger import LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient
from app.models.exceptions import DBError
from app.models.services import DictWordModel


class WordsService:
    def __init__(self, logger: LoggerBase, db_client: AsyncMongoDBBaseClient, config: Configuration):
        self.logger = logger
        self._db_name = config["mongodb"]["db_name"].get()
        self._db_collection_name = config["mongodb"]["words"]["collection_name"].get()
        self._db_client = db_client

    async def _insert_words(self, dict_words: List[DictWordModel]) -> NoReturn:
        """
        Private method which tries to store the bulk words documents into the database

        :param dict_words: list of words (DictWordModel)
        :exception DBError is been throws when failed to store the words
        """
        docs = [word.dict() for word in dict_words]
        is_inserted = await self._db_client.try_insert_many(self._db_name, self._db_collection_name, docs)
        if not is_inserted:
            raise DBError('Failed to save many words docs')

    # TODO: possible to stream the list
    async def find_similar_words(self, word: str) -> List[str]:
        """
        Find all the indexed words (from the database) which are similar to the given word param by
        comparing them to the permutation similarity index (the lexical sorted word)

        :param word: The word to find the similar other words
        :return: All the similar words
        """
        sorted_word = "".join(sorted(word))
        query = {'permutation_similarity_index': sorted_word}
        return [doc['word'] async for doc in self._db_client.find(self._db_name,
                                                                  self._db_collection_name,
                                                                  query)]

    async def count_all_words(self) -> int:
        """
        Counting all the words that are stored in the database

        :return: The number of the stored words
        """
        pipeline = [
            {'$group': {'_id': 0, 'count': {'$sum': 1}}},
        ]
        results_words = await self._db_client.aggregate(self._db_name, self._db_collection_name, pipeline)
        if results_words:
            return results_words[0]['count']
        else:
            return 0

    async def process_data_from_path_by_chunk(self, data_path: Path, chunk_size: int = 10000) -> int:
        """
        Process the dictionary words from the given file path (data_path) and stores it by bulks into the database
        in bulks

        :param data_path: The data file path which the processing is taking place
        :param chunk_size: Maximum size of the processed words to be inserted into the database
        :return: Total number of words which are processed and stored in the database
        """
        with data_path.open('r') as file_handler:
            processed_words = []
            total_words_inserted = 0
            for line in file_handler:
                # Each word is sorted lexicographical and use it as the permutation similarity index
                word = line.strip()
                if not word:
                    # if word is empty -> end of file
                    break
                sorted_word = "".join(sorted(word))
                processed_words.append(DictWordModel(word=word, permutation_similarity_index=sorted_word))
                if (num_processed_words := len(processed_words)) == chunk_size:
                    await self._insert_words(processed_words)
                    processed_words.clear()
                    total_words_inserted += num_processed_words
            if processed_words:
                await self._insert_words(processed_words)
                total_words_inserted += len(processed_words)

        return total_words_inserted
