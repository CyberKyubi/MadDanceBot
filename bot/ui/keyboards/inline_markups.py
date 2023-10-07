from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.ui.res.buttons import ButtonsText, Actions, Values


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
            text=ButtonsText.new_publication,
            callback_data=MenuCallbackFactory(action=Actions.new_publication))
        builder.button(
            text=ButtonsText.scheduled_publications,
            callback_data=MenuCallbackFactory(action=Actions.scheduled_publications))
        builder.button(
            text=ButtonsText.history_publications,
            callback_data=MenuCallbackFactory(action=Actions.history_publications))
        builder.adjust(1)
        return builder.as_markup()


class NewPublicationSectionMarkups:

    @staticmethod
    def publication_date() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=ButtonsText.today, callback_data=MenuCallbackFactory(action=Actions.today))
        builder.button(text=ButtonsText.tomorrow, callback_data=MenuCallbackFactory(action=Actions.tomorrow))
        builder.button(text=ButtonsText.back_to_main_menu, callback_data=MenuCallbackFactory(action=Actions.back_to_main_menu))
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def publication_time() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=ButtonsText.now,
            callback_data=MenuCallbackFactory(action=Actions.now, value=Values.now))

        builder.button(
            text=ButtonsText.twelve_clock,
            callback_data=MenuCallbackFactory(action=Actions.twelve_clock, value=Values.twelve_clock))
        builder.button(
            text=ButtonsText.fifteen_clock,
            callback_data=MenuCallbackFactory(action=Actions.fifteen_clock, value=Values.fifteen_clock))
        builder.button(
            text=ButtonsText.eighteen_clock,
            callback_data=MenuCallbackFactory(action=Actions.eighteen_clock, value=Values.eighteen_clock))
        builder.button(
            text=ButtonsText.five_clock,
            callback_data=MenuCallbackFactory(action=Actions.five_clock, value=Values.five_clock))

        builder.button(text=ButtonsText.back, callback_data=MenuCallbackFactory(action=Actions.back))
        builder.button(text=ButtonsText.cancel, callback_data=MenuCallbackFactory(action=Actions.cancel))
        builder.adjust(1, 3, 1, 2)
        return builder.as_markup()

    @staticmethod
    def publication_text() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=ButtonsText.back, callback_data=MenuCallbackFactory(action=Actions.back))
        builder.button(text=ButtonsText.cancel, callback_data=MenuCallbackFactory(action=Actions.cancel))
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def editing_publication_text() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=ButtonsText.schedule_publication,
            callback_data=MenuCallbackFactory(action=Actions.schedule_publication))
        builder.button(
            text=ButtonsText.cancel,
            callback_data=MenuCallbackFactory(action=Actions.cancel))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def schedule_publication() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=ButtonsText.schedule_next_publication,
            callback_data=MenuCallbackFactory(action=Actions.schedule_next_publication))
        builder.button(
            text=ButtonsText.back_to_main_menu,
            callback_data=MenuCallbackFactory(action=Actions.back_to_main_menu))
        builder.adjust(1)
        return builder.as_markup()


class ScheduledPublicationsSectionMarkup:

    @staticmethod
    def choices_publication(category: CategoriesOfPublicationsEnum) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        match category:
            case CategoriesOfPublicationsEnum.upcoming:
                builder.button(
                    text=ButtonsText.upcoming_publications,
                    callback_data=MenuCallbackFactory(action=Actions.upcoming_publications))
            case CategoriesOfPublicationsEnum.overdue:
                builder.button(
                    text=ButtonsText.overdue_publications,
                    callback_data=MenuCallbackFactory(action=Actions.overdue_publications))
            case CategoriesOfPublicationsEnum.both:
                builder.button(
                    text=ButtonsText.upcoming_publications,
                    callback_data=MenuCallbackFactory(action=Actions.upcoming_publications))
                builder.button(
                    text=ButtonsText.overdue_publications,
                    callback_data=MenuCallbackFactory(action=Actions.overdue_publications))

        builder.button(
            text=ButtonsText.back_to_main_menu,
            callback_data=MenuCallbackFactory(action=Actions.back_to_main_menu))
        builder.adjust(1)
        return builder.as_markup()
