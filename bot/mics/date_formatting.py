import pytz
from datetime import datetime, time


timezone = pytz.timezone("Europe/Samara")


def datetime_to_unix(raw_datetime: datetime) -> int:
    """
    Переводит формат даты в unix.
    :param raw_datetime:
    :return:
    """
    return int(raw_datetime.strftime('%s'))
