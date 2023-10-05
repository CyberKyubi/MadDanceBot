from sqlalchemy.engine.row import Row

from bot.data.redis.models.publications import PublicationModel
from bot.mics.date_formatting import datetime_to_unix_timestamp


def map_to_publication_model(row: Row) -> PublicationModel:
    """
    Функция для преобразования элементов Row в PublicationModel.

    Дополнительно поле "publication_at" преобразуется в unix timestamp, потому что "приходит" с типом datetime.
    :param row:
    :return: Возвращает представление данных бд в PublicationModel.
    """
    publication_id, publication_title, publication_text, publication_at, is_published = row
    publication_at = datetime_to_unix_timestamp(publication_at)
    return PublicationModel(
        publication_id=publication_id,
        publication_title=publication_title,
        publication_text=publication_text,
        publication_at=publication_at,
        is_published=is_published)
