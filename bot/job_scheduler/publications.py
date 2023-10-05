import logging

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.data.redis.models.publications import ScheduledPublicationModel
from bot.data.db.queries import select_scheduled_publications
from .jobs import send_publication_to_channel_job


async def schedule_publication(
        bot: Bot,
        scheduler: AsyncIOScheduler,
        db: async_sessionmaker[AsyncSession],
        publication: ScheduledPublicationModel
) -> None:
    """
    Планирует публикацию в канал.
    :param scheduler:
    :param bot:
    :param db:
    :param publication:
    :return:
    """
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
    publications = await select_scheduled_publications(db)
    if not publications:
        logging.info("Нет запланированных публикаций")
        return

    for publication in publications:
        await schedule_publication(bot, scheduler, db, publication)