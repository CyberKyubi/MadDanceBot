from enum import Enum

from .emoji import Emoji


class Text:
    back = f"{Emoji.back} Назад"

    new_publication = f"{Emoji.pencil2} Новая публикация"
    scheduled_publications = f"{Emoji.calendar} Запланированные публикации"
    history_publications = f"{Emoji.card_index_dividers} История публикаций"

    today = "Сегодня"
    tomorrow = "Завтра"
    now = "Сразу"
    twelve_clock = "12:00"
    fifteen_clock = "15:00"
    eighteen_clock = "18:00"
    five_clock = f"{Emoji.thief} 5:15"


class Action(str, Enum):
    back = "back"
    back_to_main_menu = "back_to_main_menu"

    new_publication = "new_publication"
    scheduled_publications = "scheduled_publications"
    history_publications = "history_publications"

    today = "today"
    tomorrow = "tomorrow"
    now = "now"
    twelve_clock = "twelve_clock"
    fifteen_clock = "fifteen_clock"
    eighteen_clock = "eighteen_clock"
    five_clock = "five_clock"


class Value:
    now = "now"
    twelve_clock = "12.0"
    fifteen_clock = "15.0"
    eighteen_clock = "18.0"
    five_clock = "5.15"











