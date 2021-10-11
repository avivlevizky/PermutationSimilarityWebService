import confuse
from confuse import Configuration
from lagom import Container

from app.core.asyncio import AsyncIOEventLoop, EventLoopBase
from app.core.logger import LoguruLogger, LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient, MotorMongoDBClient, AsyncMongoDBBaseUtilClient, MotorMongoDBUtilClient
from app.db.mongodb.util import AsyncMongoDBUtils
from app.services.stats import StatsService
from app.services.terms import TermsService


def _add_dependencies_to_container():
    container[Configuration] = confuse.Configuration('app', __name__)
    container[Configuration].set_file('config.yaml', base_for_paths=True)
    container[LoggerBase] = LoguruLogger(container[Configuration])
    container[EventLoopBase] = AsyncIOEventLoop()
    container[AsyncMongoDBBaseClient] = MotorMongoDBClient(container[LoguruLogger],
                                                           container[Configuration],
                                                           container[EventLoopBase])
    container[AsyncMongoDBBaseUtilClient] = MotorMongoDBUtilClient(container[LoguruLogger],
                                                                   container[Configuration],
                                                                   container[EventLoopBase])
    container[AsyncMongoDBUtils] = AsyncMongoDBUtils(container[LoggerBase],
                                                     container[AsyncMongoDBBaseUtilClient],
                                                     container[Configuration])
    container[StatsService] = StatsService(container[LoggerBase],
                                           container[AsyncMongoDBBaseClient],
                                           container[Configuration])
    container[TermsService] = TermsService(container[LoggerBase],
                                           container[AsyncMongoDBBaseClient],
                                           container[Configuration])


container = Container()
_add_dependencies_to_container()
