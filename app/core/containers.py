import confuse
from confuse import Configuration
from lagom import Container

from app.core.asyncio import AsyncIOEventLoop, EventLoopBase
from app.core.logger import LoguruLogger, LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient, MotorMongoDBClient, AsyncMongoDBBaseUtilClient, MotorMongoDBUtilClient
from app.db.mongodb.util import AsyncMongoDBUtils
from app.services.analytics import AnalyticsService
from app.services.words import WordsService


def _add_dependencies_to_container():
    """
    Define all the dependencies using the Lagom DI
    """
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
    container[AnalyticsService] = AnalyticsService(container[LoggerBase],
                                                   container[AsyncMongoDBBaseClient],
                                                   container[Configuration])
    container[WordsService] = WordsService(container[LoggerBase],
                                           container[AsyncMongoDBBaseClient],
                                           container[Configuration])


container = Container()     # Container which all the application dependencies are defined into it
_add_dependencies_to_container()
