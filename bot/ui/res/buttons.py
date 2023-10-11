from enum import Enum

from .emoji import Emoji


class ButtonsText:
    back = f"{Emoji.back} Назад"
    back_to_main_menu = f"{Emoji.house} Назад в главное меню"
    cancel = f"{Emoji.x} Отменить"
    back_to_section = f"{Emoji.back} Назад в раздел"
    back_to_month_selection = f"{Emoji.back} Назад к выбору месяца"
    back_to_week_selection = f"{Emoji.back} Назад к выбору недели"

    new_publication = f"{Emoji.pencil2} Новая публикация"
    scheduled_publications = f"{Emoji.calendar} Запланированные публикации"
    history_publications = f"{Emoji.card_index_dividers} История публикаций"

    today = "Сегодня"
    tomorrow = "Завтра"
    now = "Сразу"
    twelve_clock = "12:00"
    fifteen_clock = "15:00"
    eighteen_clock = "18:00"
    five_clock = f"{Emoji.thief} 05:15"
    schedule_publication = f"{Emoji.calendar} Запланировать"
    schedule_next_publication = f"{Emoji.calendar} Запланировать следующую"

    upcoming_publications = f"{Emoji.calendar} Будущие публикации"
    overdue_publications = f"{Emoji.exclamation} Просроченные публикации"

    arrow_forward = f"{Emoji.arrow_forward}"
    current_page = "{current}/{max}"
    arrow_backward = f"{Emoji.arrow_backward}"
    editing = f"{Emoji.pen} Редактирование"
    update = f"{Emoji.update} Обновить"


class Actions(str, Enum):
    back = "back"
    cancel = "cancel"
    back_to_main_menu = "back_to_main_menu"
    none = "none"

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
    schedule_publication = "schedule_publication"
    schedule_next_publication = "schedule_next_publication"

    upcoming_publications = "upcoming_publications"
    overdue_publications = "overdue_publications"

    month_selection = "month_selection"
    week_selection = "week_selection"
    back_to_section = "back_to_section"
    back_to_month_selection = "back_to_month_selection"
    back_to_week_selection = "back_to_week_selection"

    arrow_forward = "arrow_forward"
    arrow_backward = "arrow_backward"
    editing = "editing"
    update = "update"


class Values:
    now = "now"
    twelve_clock = "12.0"
    fifteen_clock = "15.0"
    eighteen_clock = "18.0"
    five_clock = "5.15"











