from aiogram import Dispatcher
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


def register_middlewares(dp: Dispatcher, redis: Redis, db_async_session: async_sessionmaker[AsyncSession]):
    from .redis_middleware import RedisMiddleware
    from .db_middleware import DBMiddleware
    from .callback_answer import CallbackAnswerMiddleware

    dp.message.middleware(RedisMiddleware(redis))
    dp.callback_query.middleware(RedisMiddleware(redis))
    dp.edited_message.middleware(RedisMiddleware(redis))

    dp.message.middleware(DBMiddleware(db_async_session))
    dp.callback_query.middleware(DBMiddleware(db_async_session))
    dp.edited_message.middleware(DBMiddleware(db_async_session))
    # dp.callback_query.middleware(CallbackAnswerMiddleware())
