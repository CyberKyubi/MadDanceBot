import logging
from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters.state import StateFilter
from magic_filter import F
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.new_publication import NewPublicationModel
from bot.data.redis.models.publications import ScheduledPublicationModel
from bot.data.db.queries import insert_new_publication
from bot.mics.date_formatting import unix_timestamp_to_datetime
from bot.job_scheduler.publications import schedule_publication
from bot.ui.res.strings import Strings
from bot.ui.res.buttons import Action
from bot.ui.keyboards.inline_markups import NewPublicationInlineMarkups, MenuCallbackFactory
from bot.ui.states.state_machine import NewPublicationStates
from bot.ui.handlers.main_menu import cmd_start
from .publication_date import new_publication_button


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back),
    NewPublicationStates.publication_time)
async def back_to_new_publication_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries) -> None:
    """
    Возвращает к первому этапу - дате публикации.
    :param query:
    :param state:
    :param redis:
    :return:
    """
    await new_publication_button(query, state, redis)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back),
    NewPublicationStates.publication_title)
async def back_to_publication_time_button(query: CallbackQuery, state: FSMContext) -> None:
    """
    Возвращает к второму этапу - времени публикации.
    :param query:
    :param state:
    :return:
    """
    await query.message.edit_text(Strings.publication_time, reply_markup=NewPublicationInlineMarkups.publication_time())
    await state.set_state(NewPublicationStates.publication_time)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back),
    NewPublicationStates.publication_text)
async def back_to_publication_title_button(query: CallbackQuery, state: FSMContext) -> None:
    """
    Возвращает к заголовку публикации.
    :param query:
    :param state:
    :return:
    """
    await query.message.edit_text(Strings.publication_title, reply_markup=NewPublicationInlineMarkups.publication_text())
    await state.set_state(NewPublicationStates.publication_title)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.cancel),
    StateFilter(NewPublicationStates))
async def cancel_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries) -> None:
    """
    Отменяет заполнение новой публикации и возвращает в главное меню.
    :param query:
    :param state:
    :param redis:
    :return:
    """
    logging.info(f"Пользователь | user_id = {query.from_user.id} | отменил заполнение публикации")

    await redis.save_new_publication(NewPublicationModel())

    await query.message.edit_text(Strings.publication_canceled)
    await cmd_start(query.message, state)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.schedule_publication),
    NewPublicationStates.editing_publication_text)
async def schedule_publication_button(
        query: CallbackQuery,
        state: FSMContext,
        redis: RedisQueries,
        db: async_sessionmaker[AsyncSession],
        scheduler: AsyncIOScheduler
) -> None:
    """

    :param query:
    :param state:
    :param redis:
    :param db:
    :param scheduler:
    :return:
    """
    model = await redis.get_new_publication()

    publication_id = await insert_new_publication(db_async_session=db, new_publication=model)
    publication_text = f"{model.publication_title}\n\n{model.publication_text}"
    publication_at = datetime.utcfromtimestamp(model.publication_at)

    schedule_publication_model = ScheduledPublicationModel(
        publication_id=publication_id,
        publication_text=publication_text,
        publication_at=publication_at)
    await schedule_publication(query.bot, scheduler, db, schedule_publication_model)

    publication_datetime = unix_timestamp_to_datetime(model.publication_at)
    await query.message.edit_text(model.publication_text)
    await query.message.answer(
        Strings.publication_info.format(title=model.publication_title, datetime=publication_datetime),
        reply_markup=NewPublicationInlineMarkups.schedule_publication())
    await state.set_state(NewPublicationStates.schedule_publication)

    await redis.save_new_publication(NewPublicationModel())

    logging.info(f"Пользователь | user_id = {query.from_user.id} | запланировал публикацию -->\n"
                 f"Info publication_id = {publication_id} | publication_at = {publication_at}")