import logging
from datetime import datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.new_publication import NewPublicationModel
from bot.mics.date_formatting import TIMEZONE
from bot.ui.res.strings import Strings, Errors
from bot.ui.res.buttons import Action
from bot.ui.keyboards.inline_markups import NewPublicationSectionMarkups, MenuCallbackFactory
from bot.ui.states.state_machine import MenuNavigationStates, NewPublicationStates


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.new_publication),
    MenuNavigationStates.main_menu)
@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.schedule_next_publication),
    NewPublicationStates.schedule_publication)
async def new_publication_button(query: CallbackQuery, state: FSMContext, redis: RedisQueries) -> None:
    """
    Запускает цепочку "Новая публикация". Первое - это дата публикации.
    :param query:
    :param state:
    :param redis:
    :return:
    """
    logging.info(f"Пользователь | user_id = {query.from_user.id} | перешел в раздел \"Новая публикация\"")
    await redis.save_new_publication(NewPublicationModel())

    await query.message.edit_text(Strings.publication_date, reply_markup=NewPublicationSectionMarkups.publication_date())
    await state.set_state(NewPublicationStates.publication_date)


@router.callback_query(
    MenuCallbackFactory.filter((F.action == Action.today) | (F.action == Action.tomorrow)),
    NewPublicationStates.publication_date)
async def publication_date_hot_buttons(
        query: CallbackQuery,
        callback_data: MenuCallbackFactory,
        state: FSMContext,
        redis: RedisQueries
) -> None:
    """
    Обрабатывает "горячие" кнопки даты публикации.
    :param query:
    :param callback_data:
    :param state:
    :param redis:
    :return:
    """
    model = await redis.get_new_publication()

    raw_date = datetime.now()
    if callback_data.action == Action.tomorrow:
        raw_date = datetime.now() + timedelta(days=1)
    local_date = raw_date.astimezone(TIMEZONE).date()

    model.raw_date = str(local_date)
    await redis.save_new_publication(model)

    await query.message.edit_text(Strings.publication_time, reply_markup=NewPublicationSectionMarkups.publication_time())
    await state.set_state(NewPublicationStates.publication_time)

    logging.info(f"Пользователь | user_id = {query.from_user.id} | указал дату = {model.raw_date}")


@router.message(NewPublicationStates.publication_date)
async def publication_date_entry(message: Message, state: FSMContext, redis: RedisQueries) -> None:
    """
    Проверяет формат введенной даты публикации.
    :param message:
    :param state:
    :param redis:
    :return:
    """
    try:
        raw_date = datetime.strptime(message.text, "%d.%m")
        publication_date = datetime(year=datetime.now().year, month=raw_date.month, day=raw_date.day).date()
    except ValueError:
        await message.answer(Errors.invalid_date_format)
        logging.error(f"Пользователь | user_id = {message.from_user.id} | указал неверный формат даты = {message.text}")
    else:
        model = await redis.get_new_publication()
        model.raw_date = str(publication_date)
        await redis.save_new_publication(model)

        await message.answer(Strings.publication_time, reply_markup=NewPublicationSectionMarkups.publication_time())
        await state.set_state(NewPublicationStates.publication_time)

        logging.info(f"Пользователь | user_id = {message.from_user.id} | указал дату = {model.raw_date}")
