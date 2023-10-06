import logging
from datetime import datetime, time

import pytz
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.mics.date_formatting import datetime_to_unix_timestamp, TIMEZONE
from bot.mics.bot_exceptions import PastPublicationTimeError
from bot.ui.res.strings import Strings, Errors
from bot.ui.res.buttons import Action, Value
from bot.ui.keyboards.inline_markups import NewPublicationSectionMarkups, MenuCallbackFactory
from bot.ui.states.state_machine import NewPublicationStates

router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(
        (F.action == Action.now) | (F.action == Action.twelve_clock) | (F.action == Action.fifteen_clock) |
        (F.action == Action.eighteen_clock) | (F.action == Action.five_clock)
    ),
    NewPublicationStates.publication_time)
async def publication_time_hot_buttons(
        query: CallbackQuery,
        callback_data: MenuCallbackFactory,
        state: FSMContext,
        redis: RedisQueries
) -> None:
    """
    Второй этап - время публикации.
    Обрабатывает "горячие" кнопки.
    :param query:
    :param callback_data:
    :param state:
    :param redis:
    :return:
    """
    if callback_data.value == Value.now:
        model = await redis.get_new_publication()
        model.is_now = True
        await redis.save_new_publication(model)

        await query.message.edit_text(Strings.publication_title, reply_markup=NewPublicationSectionMarkups.publication_text())
        await state.set_state(NewPublicationStates.publication_title)

        logging.info(f"Пользователь | user_id = {query.from_user.id} | указал время = now")
    else:
        hot_time = callback_data.value
        await publication_time_entry(query.message, state, redis, hot_time)


@router.message(NewPublicationStates.publication_time)
async def publication_time_entry(
        message: Message,
        state: FSMContext,
        redis: RedisQueries,
        hot_time: str = None
) -> None:
    """
    Собирает дату и время публикации.

    Сначала валидация введенного времени, после из "сырой" даты (например строка, 2023-10-03) собирает локальный
    datetime, и в конце приводит в UTC.

    Собранную дату и время публикации в формате UTC, бот проверяет на прошедшее время.
    :param message:
    :param state:
    :param redis:
    :param hot_time:
    :return:
    """
    model = await redis.get_new_publication()

    try:
        # Собирает время
        raw_time = datetime.strptime(message.text if not hot_time else hot_time, "%H.%M")
        publication_time = time(hour=raw_time.hour, minute=raw_time.minute)

        # Собирает дату и время
        year, month, day = map(int, model.raw_date.split("-"))
        local_date = TIMEZONE.localize(
            datetime(year=year, month=month, day=day, hour=publication_time.hour, minute=publication_time.minute))
        publication_date = local_date.astimezone(pytz.utc)

        if publication_date < datetime.now(tz=pytz.utc):
            raise PastPublicationTimeError(Errors.past_publication_time_error)

    except (ValueError, PastPublicationTimeError) as err:
        err_msg = Errors.invalid_time_format if isinstance(err, ValueError) else Errors.past_publication_time_error
        await message.answer(err_msg)
        logging.error(f"Пользователь | user_id = {message.from_user.id} |"
                      f" указал неверный формат времени или прошлое время = {message.text}")
    else:
        model.publication_at = datetime_to_unix_timestamp(publication_date)
        await redis.save_new_publication(model)

        text, reply_markup = Strings.publication_title, NewPublicationSectionMarkups.publication_text()
        if hot_time:
            await message.edit_text(text, reply_markup=reply_markup)
        else:
            await message.answer(text, reply_markup=reply_markup)
        await state.set_state(NewPublicationStates.publication_title)

        logging.info(f"Пользователь | user_id = {message.from_user.id} | дата публикации собрана = {publication_date}")
