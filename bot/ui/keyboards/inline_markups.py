from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.ui.res.buttons import Text, Action, Value


class MenuCallbackFactory(CallbackData, prefix="menu"):
    action: str
    value: Optional[str] = None


class CategoriesOfPublicationsEnum(int, Enum):
    upcoming = 0
    overdue = 1
    both = 2


class MainMenuMarkups:

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=Text.new_publication,
            callback_data=MenuCallbackFactory(action=Action.new_publication))
        builder.button(
            text=Text.scheduled_publications,
            callback_data=MenuCallbackFactory(action=Action.scheduled_publications))
        builder.button(
            text=Text.history_publications,
            callback_data=MenuCallbackFactory(action=Action.history_publications))
        builder.adjust(1)
        return builder.as_markup()


class NewPublicationSectionMarkups:

    @staticmethod
    def publication_date() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=Text.today, callback_data=MenuCallbackFactory(action=Action.today))
        builder.button(text=Text.tomorrow, callback_data=MenuCallbackFactory(action=Action.tomorrow))
        builder.button(text=Text.back_to_main_menu, callback_data=MenuCallbackFactory(action=Action.back_to_main_menu))
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def publication_time() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=Text.now,
            callback_data=MenuCallbackFactory(action=Action.now, value=Value.now))

        builder.button(
            text=Text.twelve_clock,
            callback_data=MenuCallbackFactory(action=Action.twelve_clock, value=Value.twelve_clock))
        builder.button(
            text=Text.fifteen_clock,
            callback_data=MenuCallbackFactory(action=Action.fifteen_clock, value=Value.fifteen_clock))
        builder.button(
            text=Text.eighteen_clock,
            callback_data=MenuCallbackFactory(action=Action.eighteen_clock, value=Value.eighteen_clock))
        builder.button(
            text=Text.five_clock,
            callback_data=MenuCallbackFactory(action=Action.five_clock, value=Value.five_clock))

        builder.button(text=Text.back, callback_data=MenuCallbackFactory(action=Action.back))
        builder.button(text=Text.cancel, callback_data=MenuCallbackFactory(action=Action.cancel))
        builder.adjust(1, 3, 1, 2)
        return builder.as_markup()

    @staticmethod
    def publication_text() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=Text.back, callback_data=MenuCallbackFactory(action=Action.back))
        builder.button(text=Text.cancel, callback_data=MenuCallbackFactory(action=Action.cancel))
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def editing_publication_text() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=Text.schedule_publication,
            callback_data=MenuCallbackFactory(action=Action.schedule_publication))
        builder.button(
            text=Text.cancel,
            callback_data=MenuCallbackFactory(action=Action.cancel))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def schedule_publication() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=Text.schedule_next_publication,
            callback_data=MenuCallbackFactory(action=Action.schedule_next_publication))
        builder.button(
            text=Text.back_to_main_menu,
            callback_data=MenuCallbackFactory(action=Action.back_to_main_menu))
        builder.adjust(1)
        return builder.as_markup()


class ScheduledPublicationsSectionMarkup:

    @staticmethod
    def choices_publication(category: CategoriesOfPublicationsEnum) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        match category:
            case CategoriesOfPublicationsEnum.upcoming:
                builder.button(
                    text=Text.upcoming_publications,
                    callback_data=MenuCallbackFactory(action=Action.upcoming_publications))
            case CategoriesOfPublicationsEnum.overdue:
                builder.button(
                    text=Text.overdue_publications,
                    callback_data=MenuCallbackFactory(action=Action.overdue_publications))
            case CategoriesOfPublicationsEnum.both:
                builder.button(
                    text=Text.upcoming_publications,
                    callback_data=MenuCallbackFactory(action=Action.upcoming_publications))
                builder.button(
                    text=Text.overdue_publications,
                    callback_data=MenuCallbackFactory(action=Action.overdue_publications))

        builder.button(
            text=Text.back_to_main_menu,
            callback_data=MenuCallbackFactory(action=Action.back_to_main_menu))
        builder.adjust(1)
        return builder.as_markup()
