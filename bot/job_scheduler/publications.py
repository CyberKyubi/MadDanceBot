import logging
from datetime import datetime

import pytz
from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.data.redis.models.publications import ScheduledPublicationModel
from bot.data.db.queries import select_scheduled_publications_after_start
from .jobs import send_publication_to_channel_job


async def schedule_publication(
        bot: Bot,
        scheduler: AsyncIOScheduler,
        db: async_sessionmaker[AsyncSession],
        publication: ScheduledPublicationModel,
        is_now: bool = False
) -> None:
    """
    Планирует публикацию в канал.
    :param scheduler:
    :param bot:
    :param db:
    :param publication:
    :param is_now: Указывается, когда публикация должна быть опубликована сразу.
    :return:
    """
    if is_now:
        scheduler.add_job(
            send_publication_to_channel_job,
            trigger="date",
            next_run_time=datetime.now(pytz.utc),
            args=(bot, db, publication))
        logging.info(f"Запланирована публикация --> \n"
                     f"Info: publication_id = {publication.publication_id} | publication_at = {datetime.now(pytz.utc)} UTC")
    else:
        scheduler.add_job(
            send_publication_to_channel_job,
            trigger="date",
            run_date=publication.publication_at,
            args=(bot, db, publication))
        logging.info(f"Запланирована публикация --> \n"
                     f"Info: publication_id = {publication.publication_id} | publication_at = {publication.publication_at} UTC")


async def schedule_pending_publications_after_start(
        bot: Bot,
        scheduler: AsyncIOScheduler,
        db: async_sessionmaker[AsyncSession],
) -> None:
    """
    Планирует публикации после запуска бота, если они есть.
    :param bot:
    :param scheduler:
    :param db:
    :return:
    """
    publications = await select_scheduled_publications_after_start(db)
    if not publications:
        logging.info("Нет запланированных публикаций")
        return

    for publication in publications:
        await schedule_publication(bot, scheduler, db, publication)