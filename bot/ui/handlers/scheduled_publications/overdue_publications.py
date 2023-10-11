import logging
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.publications_pages import ArchivedPublicationsPagesModel, PagesConfigModel, TypesOfPages
from bot.mics.text_formatting import format_publication_page_text
from bot.ui.handlers.publications_pages.publication_page import publication_page
from bot.ui.res.buttons import Actions
from bot.ui.states.state_machine import ScheduledPublicationsStates
from bot.ui.keyboards.inline_markups import MenuCallbackFactory, PublicationsPagesMarkup


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.overdue_publications),
    ScheduledPublicationsStates.overdue_and_upcoming_publications)
async def overdue_publications(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    category_model = await redis.get_categorized_publications()
    archived_model = ArchivedPublicationsPagesModel(publications=category_model.overdue)
    await redis.save_archived_publications_pages(archived_model)

    pages_config_model = PagesConfigModel(
        max_pages=archived_model.publications.__len__(),
        page_type=TypesOfPages.overdue_publications
    )
    await redis.save_pages_config(pages_config_model)
    await publication_page(query, state, redis, pages_config_model, archived_model=archived_model)

