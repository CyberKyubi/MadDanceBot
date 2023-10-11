import logging
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.publications import PublicationModel
from bot.data.redis.models.publications_pages import (
    TypesOfPages,
    PagesConfigModel,
    UpcomingPublicationsPagesModel,
    ArchivedPublicationsPagesModel)
from bot.mics.text_formatting import format_publication_page_text
from bot.ui.res.buttons import Actions
from bot.ui.states.state_machine import PublicationsPagesStates
from bot.ui.keyboards.inline_markups import PublicationsPagesMarkup, MenuCallbackFactory


router = Router()


async def publication_page(
        query: CallbackQuery,
        state: FSMContext,
        redis: RedisQueries,
        page_config_model: PagesConfigModel,
        upcoming_model: Optional[UpcomingPublicationsPagesModel] = None,
        archived_model: Optional[ArchivedPublicationsPagesModel] = None
):
    if page_config_model.page_type == TypesOfPages.upcoming_publications:
        upcoming_model = upcoming_model if upcoming_model else await redis.get_upcoming_publications_pages()
        publication, reply_markup = _get_upcoming_publication_case(page_config_model, upcoming_model)
    else:
        archived_model = archived_model if archived_model else await redis.get_archived_publications_pages()
        publication, reply_markup = _get_archived_publication_case(page_config_model, archived_model)

    text = format_publication_page_text(publication)
    await query.message.edit_text(text, reply_markup=reply_markup)
    await state.set_state(PublicationsPagesStates.publication_page)


def _get_upcoming_publication_case(
        page_config: PagesConfigModel,
        model: UpcomingPublicationsPagesModel
) -> tuple[PublicationModel, InlineKeyboardMarkup]:
    publication = model.period_map[model.selected_month][model.selected_week][page_config.current_page_index]
    markup_cls = PublicationsPagesMarkup(page_config)
    return publication, markup_cls.upcoming_publications()


def _get_archived_publication_case(
        page_config: PagesConfigModel,
        model: ArchivedPublicationsPagesModel
) -> tuple[PublicationModel, InlineKeyboardMarkup]:
    publication = model.publications[page_config.current_page_index]
    markup_cls = PublicationsPagesMarkup(page_config)
    return publication, markup_cls.overdue_publications()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.arrow_forward),
    PublicationsPagesStates.publication_page)
async def arrow_forward_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    config = await redis.get_pages_config()

    if config.current_page_num != config.max_pages:
        config.current_page_num += 1
        config.current_page_index += 1
        await redis.save_pages_config(config)

        await publication_page(query, state, redis, config)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.arrow_backward),
    PublicationsPagesStates.publication_page)
async def arrow_backward_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    config = await redis.get_pages_config()

    if config.current_page_num != 1:
        config.current_page_num -= 1
        config.current_page_index -= 1
        await redis.save_pages_config(config)

        await publication_page(query, state, redis, config)
