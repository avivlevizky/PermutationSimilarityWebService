import confuse
from confuse import Configuration
from lagom import Container

from app.core.asyncio import AsyncIOEventLoop, EventLoopBase
from app.core.logger import LoguruLogger, LoggerBase
from app.db.mongodb.client import AsyncMongoDBBaseClient, MotorMongoDBClient
from app.db.mongodb.util import AsyncMongoDBUtil
from app.services.stats import StatsService
from app.services.terms import TermsService


def _add_dependencies_to_container():
    container[Configuration] = confuse.sources.YamlSource('config.yaml')
    container[LoggerBase] = lambda c: LoguruLogger(c[Configuration])
    container[EventLoopBase] = AsyncIOEventLoop()
    container[AsyncMongoDBBaseClient] = lambda c: MotorMongoDBClient(c[LoguruLogger],
                                                                     c[Configuration],
                                                                     c[EventLoopBase])
    container[StatsService] = lambda c: StatsService(c[LoggerBase],
                                                     c[AsyncMongoDBBaseClient],
                                                     c[Configuration])
    container[TermsService] = lambda c: TermsService(c[LoggerBase],
                                                     c[AsyncMongoDBBaseClient],
                                                     c[Configuration])
    container[AsyncMongoDBUtil] = lambda c: AsyncMongoDBUtil(c[LoggerBase],
                                                             c[AsyncMongoDBBaseClient],
                                                             c[Configuration])


container = Container()
_add_dependencies_to_container()
