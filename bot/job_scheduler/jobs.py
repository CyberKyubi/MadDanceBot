import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramNotFound,
    TelegramForbiddenError,
    RestartingTelegram,
    TelegramAPIError,
    TelegramRetryAfter)
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.redis.models.publications import ScheduledPublicationModel
from bot.data.db.queries import update_publication_status
from bot.settings import bot_config


async def send_publication_to_channel_job(
        bot: Bot,
        db: async_sessionmaker[AsyncSession],
        publication: ScheduledPublicationModel
) -> None:
    """
    Работа для планировщика задач.
    Если отправка в канал была успешна, вызывается обновление статуса публикации.
    :param bot:
    :param db:
    :param publication:
    :return:
    """
    is_sent = await send_publication_to_channel(bot, publication.publication_text, publication.publication_id)
    if is_sent:
        await update_publication_status(db, publication.publication_id)


async def send_publication_to_channel(bot: Bot, publication: str, publication_id: int) -> bool:
    """
    Отправляет публикацию в канал.
    Отправка обернута во все возможные ошибки.
    :param bot:
    :param publication:
    :param publication_id:
    :return:
    """
    try:
        await bot.send_message(chat_id=bot_config.channel_id, text=publication)
    except (TelegramBadRequest, TelegramNotFound, TelegramForbiddenError, TelegramAPIError) as err:
        logging.error(f"Ошибка при отправки публикации в канал -->\n"
                      f"Info:\n"
                      f"publication_id = {publication_id}\n"
                      f"error = {err}")
    except (RestartingTelegram, TelegramRetryAfter) as err:
        logging.error(f"Ошибка при отправки публикации в канал -->\n"
                      f"Info:\n"
                      f"publication_id = {publication_id}\n"
                      f"error = {err}\n"
                      f"action = retry after sleep for 5 seconds")
        await asyncio.sleep(5)
        await send_publication_to_channel(bot, publication, publication_id)
    else:
        logging.info(f"Успешная отправка публикации в канал --> publication_id = {publication_id}")
        return True
    return False
