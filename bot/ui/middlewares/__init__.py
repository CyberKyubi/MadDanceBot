from aiogram import Dispatcher
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def register_middlewares(
        dp: Dispatcher,
        redis: Redis,
        db_async_session: async_sessionmaker[AsyncSession],
        scheduler: AsyncIOScheduler
):
    # from .callback_answer import CallbackAnswerMiddleware
    from .redis_middleware import RedisMiddleware
    from .db_middleware import DBMiddleware
    from .scheduler_middleware import SchedulerMiddleware

    # dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.message.middleware(RedisMiddleware(redis))
    dp.callback_query.middleware(RedisMiddleware(redis))
    dp.edited_message.middleware(RedisMiddleware(redis))

    dp.message.middleware(DBMiddleware(db_async_session))
    dp.callback_query.middleware(DBMiddleware(db_async_session))

    dp.message.middleware(SchedulerMiddleware(scheduler))
    dp.callback_query.middleware(SchedulerMiddleware(scheduler))

