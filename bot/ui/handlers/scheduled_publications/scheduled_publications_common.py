import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from magic_filter import F
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.publications_pages import PagesConfigModel, TypesOfPages
from bot.ui.res.buttons import Actions
from bot.ui.keyboards.inline_markups import MenuCallbackFactory, NavigationBackButton
from bot.ui.states.state_machine import ScheduledPublicationsStates, PublicationsPagesStates
from .scheduled_publications import find_upcoming_or_overdue_publications
from .upcoming_publications import month_gap_case, week_ranges_case, PeriodCasesArgs


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.back_to_section),
    StateFilter(
        ScheduledPublicationsStates.month_selection,
        ScheduledPublicationsStates.week_selection,
        PublicationsPagesStates.publication_page
    ))
async def back_to_section_of_scheduled_publication_button(
        query: CallbackQuery,
        state: FSMContext,
        redis: RedisQueries,
        db: async_sessionmaker[AsyncSession],
):
    await find_upcoming_or_overdue_publications(query, state, redis, db)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.back_to_month_selection),
    ScheduledPublicationsStates.week_selection
)
async def back_to_month_selection_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    model = await redis.get_upcoming_publications_pages()

    month_names = tuple(model.period_map.keys())
    await month_gap_case(args=PeriodCasesArgs(query, state, month_names=month_names))


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.back_to_week_selection),
    PublicationsPagesStates.publication_page)
async def back_to_week_selection_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    model = await redis.get_upcoming_publications_pages()
    month_names = tuple(model.period_map.keys())
    back_button_args = NavigationBackButton.back_to_section() if len(month_names) == 1 else NavigationBackButton.back_to_month()

    week_ranges = tuple(model.period_map[model.selected_month].keys())
    await week_ranges_case(args=PeriodCasesArgs(query, state, week_ranges=week_ranges, back_button_args=back_button_args))

