import logging
from datetime import datetime, timedelta

import pytz
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.publications import PublicationModel, CategorizedPublicationsModel
from bot.data.db.queries import select_upcoming_publications, select_overdue_unpublished_publications
from bot.mics.text_formatting import generate_text_list_of_publications
from bot.ui.res.strings import Strings
from bot.ui.res.buttons import Actions
from bot.ui.keyboards.inline_markups import (
    ScheduledPublicationsSectionMarkup, MenuCallbackFactory, CategoriesOfPublicationsEnum)
from bot.ui.states.state_machine import MenuNavigationStates, ScheduledPublicationsStates


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Actions.upcoming_publications),
    ScheduledPublicationsStates.overdue_and_upcoming_publications)
async def upcoming_publication_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries):
    model = await redis.get_categorized_publications()