from confuse import Configuration
from pathlib import Path

import pytest

from fastapi.testclient import TestClient
from app.core.containers import container

from app.main import fastapi_app
from app.services.words import WordsService
from app.core.asyncio import EventLoopBase


client = TestClient(fastapi_app)
PREFIX_ENDPOINT = container[Configuration]["app"]["api_router"]["prefix"].get()


@pytest.fixture
def add_mock_data():
    data_file_path = container[Configuration]['data']['file_path'].get()
    process_data_coroutine = container[WordsService].process_data_from_path_by_chunk(Path(data_file_path))
    container[EventLoopBase].run(process_data_coroutine)


def test_stats_without_mocked_data():
    response = client.get(f"{PREFIX_ENDPOINT}/stats")
    assert response.status_code == 200
    assert response.json() == {'totalWords': 0, 'totalRequests': 0, 'avgProcessingTimeNs': None}


def test_similar_without_mocked_data():
    response = client.get(f"{PREFIX_ENDPOINT}/similar?word=a")
    assert response.status_code == 200
    assert response.json() == {"similar": []}


def test_similar_with_mocked_data(add_mock_data):
    response = client.get(f"{PREFIX_ENDPOINT}/similar?word=a")
    assert response.status_code == 200
    assert response.json() == {"similar": ['a']}


def test_stats_with_mocked_data():
    client.get(f"{PREFIX_ENDPOINT}/similar?word=a")
    response = client.get(f"{PREFIX_ENDPOINT}/stats")
    assert response.status_code == 200
    response_as_json = response.json()
    assert response_as_json['totalWords'] == 111
    assert response_as_json['totalRequests'] == 3
    assert type(response_as_json['avgProcessingTimeNs']) is float
