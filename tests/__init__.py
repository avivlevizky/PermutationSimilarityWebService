from confuse import Configuration

from app.core.containers import container
from app.core.asyncio import EventLoopBase
from app.db.mongodb.util import AsyncMongoDBUtils
from app.db.mongodb.client import AsyncMongoDBBaseUtilClient
from app.core.logger import LoggerBase
from app.services.words import WordsService
from app.services.analytics import AnalyticsService


async def init():
    config = container[Configuration]
    logger = container[LoggerBase]
    config.set_file('tests/config.yaml', base_for_paths=True)

    tests_db_name = config['mongodb']['db_name'].get()
    logger.info(f"Creating mocked mongodb collections in {tests_db_name} database")
    await container[AsyncMongoDBUtils].create_indexes(tests_db_name)

    logger.info("Monkey patching the services with the tests database")
    container[WordsService]._db_name = tests_db_name
    container[AnalyticsService]._db_name = tests_db_name


async def cleanup():
    tests_db_name = container[Configuration]['mongodb']['db_name'].get()
    await container[AsyncMongoDBBaseUtilClient].drop_db(tests_db_name)


def setup_module():
    """ setup any state specific to the execution of the given module."""
    container[EventLoopBase].run(init())


def teardown_module():
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    container[EventLoopBase].run(cleanup())
