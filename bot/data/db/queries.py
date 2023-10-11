import logging

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, func, and_

from bot.data.redis.models.new_publication import NewPublicationModel
from bot.data.redis.models.publications import PublicationModel, ScheduledPublicationModel
from bot.mics.date_formatting import datetime_utcnow
from .models import Publications
from .mappers import map_to_publication_model


async def insert_new_publication(db_async_session: async_sessionmaker[AsyncSession], new_publication: NewPublicationModel) -> int:
    """
    Добавляет новую публикацию и возвращает ее id.
    :param db_async_session:
    :param new_publication:
    :return: publication_id
    """
    logging.info("Выполнение запроса: insert_new_publication")

    async with db_async_session() as session:
        query = await session.execute(
            insert(Publications)
            .values(
                publication_title=new_publication.publication_title,
                publication_text=new_publication.publication_text,
                publication_at=func.to_timestamp(new_publication.publication_at))
            .returning(Publications.publication_id)
        )
        await session.commit()
        return query.one()[0]


async def select_upcoming_publications(db_async_session: async_sessionmaker[AsyncSession]) -> tuple[PublicationModel, ...] | None:
    """
    Забирает все будущие публикации по возрастанию даты.
    :param db_async_session:
    :return: При успехе возвращает картеж из PublicationModel.
    """
    logging.info("Выполнение запроса: select_upcoming_publications")

    current_time = datetime_utcnow()

    async with db_async_session() as session:
        query = await session.execute(
            select(
                Publications.publication_id,
                Publications.publication_title,
                Publications.publication_text,
                Publications.publication_at,
                Publications.is_published)
            .where(
                and_(
                    Publications.is_published.is_(False),
                    current_time < Publications.publication_at))
            .order_by(
                Publications.publication_at.asc())
        )
        if query:
            return tuple(map(map_to_publication_model, query.all()))
    return


async def select_overdue_unpublished_publications(db_async_session: async_sessionmaker[AsyncSession]) -> tuple[PublicationModel, ...] | None:
    """
    Забирает просроченные публикации по возрастанию даты.
    :param db_async_session:
    :return: При успехе возвращает картеж из PublicationModel.
    """
    logging.info("Выполнение запроса: select_overdue_unpublished_publications")

    current_time = datetime_utcnow()

    async with db_async_session() as session:
        query = await session.execute(
            select(
                Publications.publication_id,
                Publications.publication_title,
                Publications.publication_text,
                Publications.publication_at,
                Publications.is_published)
            .where(
                and_(
                    Publications.is_published.is_(False),
                    current_time > Publications.publication_at))
            .order_by(
                Publications.publication_at.asc())
        )
        if query:
            return tuple(map(map_to_publication_model, query.all()))
    return


async def update_publication_status(db_async_session: async_sessionmaker[AsyncSession], publication_id: int) -> None:
    """
    Обновляет статус публикации.
    :param db_async_session:
    :param publication_id:
    :return:
    """
    logging.info("Выполнение запроса: update_publication_status")

    async with db_async_session() as session:
        await session.execute(
            update(Publications)
            .where(Publications.publication_id == publication_id)
            .values({"is_published": True})
        )
        await session.commit()


async def select_scheduled_publications_after_start(db_async_session: async_sessionmaker[AsyncSession]) -> tuple[ScheduledPublicationModel] | None:
    """
    Функция вызывается после старта бота. Данные передаются в apscheduler.
    :param db_async_session:
    :return: При успехе возвращает список ScheduledPublicationModel.
    """
    logging.info("Выполнение запроса: select_scheduled_publications")

    current_time = datetime_utcnow()

    async with db_async_session() as session:
        query = await session.execute(
            select(
                Publications.publication_id,
                Publications.publication_text,
                Publications.publication_at)
            .where(
                and_(
                    Publications.is_published.is_(False),
                    current_time < Publications.publication_at))
            .order_by(
                Publications.publication_at.asc())
        )
        if query:
            return tuple(ScheduledPublicationModel(**model) for model in query.mappings().all())
    return