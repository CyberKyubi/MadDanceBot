import pytz
from datetime import datetime


TIMEZONE = pytz.timezone("Europe/Samara")


def datetime_to_unix_timestamp(raw_datetime: datetime) -> int:
    """
    Переводит формат даты в unix_timestamp.
    :param raw_datetime:
    :return:
    """
    return int(raw_datetime.strftime('%s'))


def unix_timestamp_to_datetime(unix: int) -> str:
    utc_datetime = datetime.utcfromtimestamp(unix)
    return utc_datetime.astimezone(TIMEZONE).strftime('%d.%m.%Y %H:%M:%S')
