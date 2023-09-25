from aiogram import Dispatcher
from redis.asyncio.client import Redis


def register_middlewares(dp: Dispatcher, redis: Redis):
    from .redis_middleware import RedisMiddleware
    from .callback_answer import CallbackAnswerMiddleware

    dp.message.middleware(RedisMiddleware(redis))
    dp.callback_query.middleware(RedisMiddleware(redis))
    dp.edited_message.middleware(RedisMiddleware(redis))
    # dp.callback_query.middleware(CallbackAnswerMiddleware())
