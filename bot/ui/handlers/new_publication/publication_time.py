from datetime import datetime, time, timedelta

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
from bot.ui.keyboards.inline_markups import NewPublicationInlineMarkups, MenuCallbackFactory
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

        await query.message.edit_text(Strings.publication_text, reply_markup=NewPublicationInlineMarkups.publication_text())
        await state.set_state(NewPublicationStates.publication_text)
    else:
        hot_time = callback_data.value
        await publication_time_entry(query.message, state, redis, hot_time)


@router.message(NewPublicationStates.publication_time)
async def publication_time_entry(message: Message, state: FSMContext, redis: RedisQueries, hot_time: str = None) -> None:
    """
    Проверяет формат введенного времени публикации.
    Дополнительная проверка на прошедшее время.
    :param message:
    :param state:
    :param redis:
    :param hot_time:
    :return:
    """
    model = await redis.get_new_publication()
    try:
        raw_time = datetime.strptime(message.text if not hot_time else hot_time, "%H.%M")
        publication_time = time(hour=raw_time.hour, minute=raw_time.minute)

        (year, month, day) = map(int, model.raw_date.split("-"))
        local_date = TIMEZONE.localize(
            datetime(
                year=year,
                month=month,
                day=day,
                hour=publication_time.hour,
                minute=publication_time.minute))
        publication_date = local_date.astimezone(pytz.utc)
        print(publication_date, datetime.now(tz=pytz.utc))
        # todo время может быть будущем но в прошлом дне.
        if publication_date < datetime.now(tz=pytz.utc):
            raise PastPublicationTimeError(Errors.past_publication_time_error)
    except ValueError:
        await message.answer(Errors.invalid_time_format)
    except PastPublicationTimeError:
        await message.answer(Errors.past_publication_time_error)
    else:
        model.unix_timestamp = datetime_to_unix_timestamp(publication_date)
        await redis.save_new_publication(model)

        await message.edit_text(Strings.publication_title, reply_markup=NewPublicationInlineMarkups.publication_text())
        await state.set_state(NewPublicationStates.publication_title)
