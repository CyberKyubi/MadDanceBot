import logging
from datetime import datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.new_publication import NewPublicationModel
from bot.data.redis.models.publications import PublicationModel
from bot.data.db.queries import select_upcoming_publications, select_overdue_unpublished_publications
from bot.mics.date_formatting import TIMEZONE
from bot.mics.text_formatting import generate_text_list_of_publications
from bot.ui.res.strings import Strings
from bot.ui.res.buttons import Action
from bot.ui.keyboards.inline_markups import (
    ScheduledPublicationsSectionMarkup, MenuCallbackFactory, CategoriesOfPublicationsEnum)
from bot.ui.states.state_machine import MenuNavigationStates, ScheduledPublicationsStates


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.scheduled_publications),
    MenuNavigationStates.main_menu)
async def find_upcoming_or_overdue_publications(
        query: CallbackQuery,
        state: FSMContext,
        db: async_sessionmaker[AsyncSession],
):
    """
    Извлекает из базы данных информацию о будущих и просроченных публикациях.

    - При наличии публикаций в обеих категориях: формирует общий текстовый список, объединяя данные из обеих групп.
    - При наличии публикаций только в одной категории: формирует текстовый список только для этой группы.

    В зависимости от доступных категорий публикаций формирует соответствующие кнопки для интерфейса:
    - Если доступны обе категории: создает кнопки для обеих групп.
    - Если доступна только одна категория: создает кнопку только для этой группы.
    :param query:
    :param state:
    :param db:
    :return:
    """
    upcoming_publications = await select_upcoming_publications(db)
    overdue_publications = await select_overdue_unpublished_publications(db)

    text_list, markup_types = build_response(upcoming_publications, overdue_publications)
    if not text_list:
        await query.answer(Strings.no_upcoming_publications)
        return

    reply_markup_mapper = {
        ("upcoming", ): ScheduledPublicationsSectionMarkup.choices_publication(
            category=CategoriesOfPublicationsEnum.upcoming),
        ("overdue", ): ScheduledPublicationsSectionMarkup.choices_publication(
            category=CategoriesOfPublicationsEnum.overdue),
        ("upcoming", "overdue"): ScheduledPublicationsSectionMarkup.choices_publication(
            category=CategoriesOfPublicationsEnum.both)
    }
    text = Strings.section_of_scheduled_publication + text_list
    reply_markup = reply_markup_mapper[tuple(markup_types)]

    await query.message.edit_text(text, reply_markup=reply_markup)
    await state.set_state(ScheduledPublicationsStates.overdue_and_upcoming_publications)


def build_response(upcoming: tuple[PublicationModel] | None, overdue: tuple[PublicationModel] | None) -> tuple[str, list[str]]:
    """
    Собирает текст и кнопки в зависимости от переданных аргументов.
    :param upcoming:
    :param overdue:
    :return:
    """
    text_parts = []
    markup_types = []

    if upcoming:
        text_parts.append(collect_text_list_of_publications(upcoming, category=CategoriesOfPublicationsEnum.upcoming))
        markup_types.append('upcoming')
    if overdue:
        text_parts.append(collect_text_list_of_publications(overdue, category=CategoriesOfPublicationsEnum.overdue))
        markup_types.append('overdue')

    return "".join(text_parts), markup_types


def collect_text_list_of_publications(publications: tuple[PublicationModel], category: CategoriesOfPublicationsEnum) -> str:
    """
    Собирает текстовый список публикаций в зависимости от категории.
    :param publications:
    :param category: Группы публикаций.
    Группа "upcoming" - это будущие публикации.
    Группа "overdue" - это просроченные публикации.
    :return: Возвращает строку из списка публикаций.
    """
    text_list = generate_text_list_of_publications(publications)
    match category:
        case CategoriesOfPublicationsEnum.upcoming:
            return Strings.list_of_upcoming_publications.format(text_list)
        case CategoriesOfPublicationsEnum.overdue:
            return Strings.list_of_overdue_publications.format(text_list)
