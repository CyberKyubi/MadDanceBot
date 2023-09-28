from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update, func

from .models import Publications
from bot.data.redis.models.new_publication import NewPublicationModel


async def insert_new_publication(
        db_async_session: async_sessionmaker[AsyncSession],
        new_publication: NewPublicationModel
) -> None:
    """
    Добавляет новую публикацию.
    :param db_async_session:
    :param new_publication:
    :return:
    """
    async with db_async_session() as session:
        await session.execute(
            insert(Publications)
            .values(
                unix_timestamp=func.to_timestamp(new_publication.unix_timestamp),
                title=new_publication.title,
                text=new_publication.text)
            .on_conflict_do_nothing())
        await session.commit()

