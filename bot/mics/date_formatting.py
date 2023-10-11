from datetime import datetime, timedelta
from collections import defaultdict

import pytz

from bot.data.redis.models.publications import PublicationModel
from bot.data.redis.models.publications_pages import PublicationMonthMap

TIMEZONE = pytz.timezone("Europe/Samara")
MONTHS = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

MONTH_GENT = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря",
}

WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}


def datetime_utcnow() -> datetime:
    """
    Возвращает текущее время в UTC.
    :return:
    """
    return datetime.now(pytz.utc)


def datetime_to_unix_timestamp(raw_datetime: datetime) -> int:
    """
    Переводит формат даты в unix_timestamp.
    :param raw_datetime:
    :return:
    """
    return int(raw_datetime.strftime('%s'))


def unix_timestamp_to_datetime(unix: int) -> datetime:
    """
    Переводит unix timestamp в дату UTC.
    :param unix:
    :return:
    """
    return datetime.utcfromtimestamp(unix)


def unix_timestamp_to_beautiful_local_date(unix: int):
    """

    :param unix:
    :return:
    """
    utc_datetime = unix_timestamp_to_datetime(unix)
    local_date = utc_datetime.astimezone(TIMEZONE)

    return ("     <b>—</b> {day_of_week}, {day} {month}\n"
            "     <b>—</b> {hour}:{minutes:02}").format(
        day_of_week=WEEKDAYS[local_date.weekday()],
        day=local_date.day,
        month=MONTH_GENT[local_date.month],
        hour=local_date.hour,
        minutes=local_date.minute
    )


def group_publication_by_month_and_week(publications: tuple[PublicationModel, ...]) -> PublicationMonthMap:
    """
    Группирует публикации по месяцам и неделям.
    :param publications:
    :return:
    """
    publications_by_month_and_week = defaultdict(lambda: defaultdict(list))

    for publication in publications:
        publication_at = unix_timestamp_to_datetime(publication.publication_at)
        month_name = MONTHS[publication_at.month]
        week_range = get_week_range_str(publication_at)

        publications_by_month_and_week[month_name][week_range].append(publication)

    return publications_by_month_and_week


def get_week_range_str(publication_date: datetime) -> str:
    """
    Получает неделю из даты.
    :param publication_date:
    :return:
    """
    day_of_week = publication_date.weekday()
    beginning_of_week = publication_date - timedelta(days=day_of_week)
    end_of_week = publication_date + timedelta(days=6 - day_of_week)

    return f"{beginning_of_week.day}.{beginning_of_week.month} — {end_of_week.day}.{end_of_week.month}"

