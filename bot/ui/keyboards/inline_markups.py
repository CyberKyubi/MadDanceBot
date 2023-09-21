from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.ui.res.buttons import Text, Action, Value


class MenuCallbackFactory(CallbackData, prefix="menu"):
    action: str
    value: Optional[str] = None


class BaseInlineMarkups:

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


class NewPublicationInlineMarkups:

    @staticmethod
    def publication_date() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=Text.today, callback_data=MenuCallbackFactory(action=Action.today))
        builder.button(text=Text.tomorrow, callback_data=MenuCallbackFactory(action=Action.tomorrow))
        builder.button(text=Text.back, callback_data=MenuCallbackFactory(action=Action.back_to_main_menu))
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
        builder.adjust(1, 3, 1)
        return builder.as_markup()
