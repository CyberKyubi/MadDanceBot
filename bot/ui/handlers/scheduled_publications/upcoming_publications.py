import logging

from dataclasses import dataclass, field
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.publications_pages import UpcomingPublicationsPagesModel, PagesConfigModel, TypesOfPages
from bot.mics.date_formatting import group_publication_by_month_and_week
from bot.ui.res.strings import Strings
from bot.ui.res.buttons import Actions
from bot.ui.states.state_machine import ScheduledPublicationsStates
from bot.ui.keyboards.inline_markups import (
    PublicationPeriodMarkup,
    MenuCallbackFactory,
    NavigationBackButton,
    BackButtonArgs)
from bot.ui.handlers.publications_pages.publication_page import publication_page


router = Router()


@dataclass
class PeriodCasesArgs:
    query: CallbackQuery
    state: FSMContext
    back_button_args: BackButtonArgs = field(default_factory=NavigationBackButton.back_to_section)
    month_names: Optional[tuple[str]] = None
    week_ranges: Optional[tuple[str]] = None


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.upcoming_publications),
    ScheduledPublicationsStates.overdue_and_upcoming_publications)
async def upcoming_publication_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    model = await redis.get_categorized_publications()
    period_map = group_publication_by_month_and_week(model.upcoming)
    await redis.save_upcoming_publications_pages(UpcomingPublicationsPagesModel(period_map=period_map))

    month_names = tuple(period_map.keys())

    if len(month_names) == 1:
        week_ranges = tuple(period_map[month_names[0]].keys())
        await week_ranges_case(args=PeriodCasesArgs(query, state, week_ranges=week_ranges))
    else:
        await month_gap_case(args=PeriodCasesArgs(query, state, month_names=month_names))


async def month_gap_case(args: PeriodCasesArgs):
    markup_cls = PublicationPeriodMarkup()
    reply_markup = markup_cls.build_month_buttons(months_name=args.month_names, back_button_args=args.back_button_args)
    await args.query.message.edit_text(Strings.month_gap, reply_markup=reply_markup)
    await args.state.set_state(ScheduledPublicationsStates.month_selection)


async def week_ranges_case(args: PeriodCasesArgs):
    markup_cls = PublicationPeriodMarkup()
    reply_markup = markup_cls.build_week_buttons(week_ranges=args.week_ranges, back_button_args=args.back_button_args)
    await args.query.message.edit_text(Strings.week_range, reply_markup=reply_markup)
    await args.state.set_state(ScheduledPublicationsStates.week_selection)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.month_selection),
    ScheduledPublicationsStates.month_selection)
async def process_month_selection(
        query: CallbackQuery,
        callback_data: MenuCallbackFactory,
        state: FSMContext,
        redis: RedisQueries
):
    model = await redis.get_upcoming_publications_pages()
    selected_month = callback_data.value
    model.selected_month = selected_month
    await redis.save_upcoming_publications_pages(model)

    week_ranges = tuple(model.period_map[selected_month].keys())
    await week_ranges_case(args=PeriodCasesArgs(
        query, state, week_ranges=week_ranges, back_button_args=NavigationBackButton.back_to_month()))


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.week_selection),
    ScheduledPublicationsStates.week_selection)
async def process_week_selection(
        query: CallbackQuery,
        callback_data: MenuCallbackFactory,
        state: FSMContext,
        redis: RedisQueries
):
    upcoming_model = await redis.get_upcoming_publications_pages()
    selected_week = callback_data.value
    upcoming_model.selected_week = selected_week
    await redis.save_upcoming_publications_pages(upcoming_model)

    pages_config_model = PagesConfigModel(
        max_pages=upcoming_model.period_map[upcoming_model.selected_month][upcoming_model.selected_week].__len__(),
        page_type=TypesOfPages.upcoming_publications
    )
    await redis.save_pages_config(pages_config_model)
    await publication_page(query, state, redis, pages_config_model, upcoming_model=upcoming_model)

