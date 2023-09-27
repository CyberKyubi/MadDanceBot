from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters.state import StateFilter
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.new_publication import NewPublicationModel
from bot.mics.date_formatting import unix_to_datetime
from bot.ui.res.strings import Strings
from bot.ui.res.buttons import Action
from bot.ui.keyboards.inline_markups import NewPublicationInlineMarkups, MenuCallbackFactory
from bot.ui.states.state_machine import NewPublicationStates
from .publication_date import new_publication
from bot.ui.handlers.main_menu import cmd_start


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back),
    NewPublicationStates.publication_time)
async def back_to_new_publication(query: CallbackQuery, state: FSMContext) -> None:
    """
    Возвращает к первому этапу - дате публикации.
    :param query:
    :param state:
    :return:
    """
    await new_publication(query, state)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back),
    NewPublicationStates.publication_text)
async def back_to_publication_time(query: CallbackQuery, state: FSMContext) -> None:
    """
    Возвращает к второму этапу - времени публикации.
    :param query:
    :param state:
    :return:
    """
    await query.message.edit_text(Strings.publication_time, reply_markup=NewPublicationInlineMarkups.publication_time())
    await state.set_state(NewPublicationStates.publication_time)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.cancel),
    StateFilter(NewPublicationStates))
async def cancel(query: CallbackQuery, state: FSMContext, redis: RedisQueries) -> None:
    """
    Отменяет заполнение новой публикации и возвращает в главное меню.
    :param query:
    :param state:
    :param redis:
    :return:
    """
    await redis.save_new_publication(NewPublicationModel())

    await query.message.edit_text(Strings.publication_canceled)
    await cmd_start(query.message, state)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.schedule_publication),
    NewPublicationStates.editing_publication_text)
async def schedule_publication(query: CallbackQuery, state: FSMContext, redis: RedisQueries) -> None:
    model = await redis.get_new_publication()
    await query.message.edit_text(model.text)

    # todo запланировать публикацию

    publication_datetime = unix_to_datetime(model.datetime)
    print(model.datetime)
    await query.message.answer(
        Strings.publication_info.format(datetime=publication_datetime),
        reply_markup=NewPublicationInlineMarkups.schedule_publication())
    await state.set_state(NewPublicationStates.schedule_publication)