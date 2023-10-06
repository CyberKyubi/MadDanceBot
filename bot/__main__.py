import asyncio
import logging
from logging.config import dictConfig

import ujson
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.settings import bot_config
from bot.job_scheduler.publications import schedule_pending_publications_after_start
from bot.mics.log_config import log_config
from bot.data.redis.base import RedisBase
from bot.data.db.base import metadata
from bot.ui.handlers import setup_routers
from bot.ui.middlewares import register_middlewares


logging.getLogger(__name__)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
dictConfig(log_config)


async def main():
    redis_base = RedisBase(dsn=bot_config.redis_dsn.__str__())
    redis = await redis_base.connect()

    engine = create_async_engine(url=bot_config.postgres_uri.__str__(), future=True, echo=False)
    db_async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    scheduler = AsyncIOScheduler()
    scheduler.start()

    bot = Bot(token=bot_config.token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=RedisStorage(redis=redis, json_loads=ujson.loads, json_dumps=ujson.dumps))

    router = setup_routers()
    dp.include_router(router)
    register_middlewares(dp, redis, db_async_session, scheduler)

    # Планирует публикации.
    await schedule_pending_publications_after_start(bot, scheduler, db_async_session)

    try:
        await dp.start_polling(bot)
    except Exception as err:
        logging.error(err)
    finally:
        await redis_base.disconnect()
        await engine.dispose()
        await scheduler.shutdown()

        await bot.session.close()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.error('Bot is stopped!')
