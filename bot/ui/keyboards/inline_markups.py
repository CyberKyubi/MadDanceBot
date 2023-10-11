from dataclasses import dataclass
from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.redis.models.publications_pages import PagesConfigModel
from bot.ui.res.buttons import ButtonsText, Actions, Values


class MenuCallbackFactory(CallbackData, prefix="menu"):
    action: str
    value: Optional[str] = None


class CategoriesOfPublicationsEnum(int, Enum):
    upcoming = 0
    overdue = 1
    both = 2


@dataclass
class BackButtonArgs:
    text: str
    action: str


@dataclass
class NavigationBackButton:
    @staticmethod
    def back_to_section() -> BackButtonArgs:
        return BackButtonArgs(text=ButtonsText.back_to_section, action=Actions.back_to_section)

    @staticmethod
    def back_to_month() -> BackButtonArgs:
        return BackButtonArgs(text=ButtonsText.back_to_month_selection, action=Actions.back_to_month_selection)


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


class PublicationPeriodMarkup:

    def build_month_buttons(self, months_name: tuple[str], back_button_args: BackButtonArgs) -> InlineKeyboardMarkup:
        """

        :param months_name:
        :param back_button_args:
        :return:
        """
        builder = InlineKeyboardBuilder()

        for month_name in months_name:
            builder.button(text=month_name, callback_data=MenuCallbackFactory(action=Actions.month_selection, value=month_name))

        builder.adjust(3)
        builder.attach(self._build_last_back_button(back_button_args))
        return builder.as_markup()

    def build_week_buttons(self, week_ranges: tuple[str], back_button_args: BackButtonArgs) -> InlineKeyboardMarkup:
        """

        :param week_ranges:
        :param back_button_args:
        :return:
        """
        builder = InlineKeyboardBuilder()

        for week in week_ranges:
            builder.button(text=week, callback_data=MenuCallbackFactory(action=Actions.week_selection, value=week))

        builder.adjust(2)
        builder.attach(self._build_last_back_button(back_button_args))
        return builder.as_markup()

    @staticmethod
    def _build_last_back_button(args: BackButtonArgs) -> InlineKeyboardBuilder:
        """

        :param args:
        :return:
        """
        back_builder = InlineKeyboardBuilder()
        back_builder.button(text=args.text, callback_data=MenuCallbackFactory(action=args.action))
        back_builder.adjust(1)
        return back_builder


class PublicationsPagesMarkup:
    def __init__(self, pages_config: PagesConfigModel):
        self.pages_config = pages_config

    def upcoming_publications(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder_base_buttons = self._build_base_pages_buttons()
        builder.attach(builder_base_buttons)

        builder.button(text=ButtonsText.editing,
                       callback_data=MenuCallbackFactory(action=Actions.editing))
        builder.button(text=ButtonsText.back_to_week_selection,
                       callback_data=MenuCallbackFactory(action=Actions.back_to_week_selection))
        builder.button(text=ButtonsText.back_to_main_menu,
                       callback_data=MenuCallbackFactory(action=Actions.back_to_main_menu))

        builder.adjust(3, 1)
        return builder.as_markup()

    def overdue_publications(self):
        builder = InlineKeyboardBuilder()
        builder_base_buttons = self._build_base_pages_buttons()
        builder.attach(builder_base_buttons)

        builder.button(text=ButtonsText.update,
                       callback_data=MenuCallbackFactory(action=Actions.update))
        builder.button(text=ButtonsText.back_to_section,
                       callback_data=MenuCallbackFactory(action=Actions.back_to_section))
        builder.button(text=ButtonsText.back_to_main_menu,
                       callback_data=MenuCallbackFactory(action=Actions.back_to_main_menu))

        builder.adjust(3, 1)
        return builder.as_markup()

    def published(self):
        builder = InlineKeyboardBuilder()
        builder_base_buttons = self._build_base_pages_buttons()
        builder.attach(builder_base_buttons)

        builder.button(text=ButtonsText.back_to_main_menu,
                       callback_data=MenuCallbackFactory(action=Actions.back_to_main_menu))

        builder.adjust(3, 1)
        return builder.as_markup()

    def _build_base_pages_buttons(self) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()

        builder.button(text=ButtonsText.arrow_backward, callback_data=MenuCallbackFactory(action=Actions.arrow_backward))
        builder.button(
            text=ButtonsText.current_page.format(
                current=self.pages_config.current_page_num,
                max=self.pages_config.max_pages),
            callback_data=MenuCallbackFactory(action=Actions.none))
        builder.button(text=ButtonsText.arrow_forward, callback_data=MenuCallbackFactory(action=Actions.arrow_forward))

        return builder
