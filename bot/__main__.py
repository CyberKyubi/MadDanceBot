import asyncio
import logging
from logging.config import dictConfig

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.settings import bot_config
from bot.mics.log_config import log_config
from bot.data.redis.Base import RedisBase
from bot.ui.handlers import setup_routers


logging.getLogger(__name__)
dictConfig(log_config)


async def main():
    redis_base = RedisBase(dsn=str(bot_config.redis_dsn))
    redis = await redis_base.connect()

    bot = Bot(token=bot_config.token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    router = setup_routers()
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except Exception as err:
        logging.error(err)
    finally:
        await redis_base.disconnect()

        await bot.session.close()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.error('Bot is stopped!')
