from datetime import datetime, time

import pytz
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.mics.date_formatting import datetime_to_unix, TIMEZONE
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
        print(model)

    else:
        hot_time = callback_data.value
        await publication_time_entry(query.message, state, redis, hot_time)


@router.message(NewPublicationStates.publication_time)
async def publication_time_entry(message: Message, state: FSMContext, redis: RedisQueries, hot_time: str = None) -> None:
    """
    Проверяет формат введенного времени публикации.
    :param message:
    :param state:
    :param redis:
    :param hot_time:
    :return:
    """
    try:
        raw_time = datetime.strptime(message.text if not hot_time else hot_time, "%H.%M")
        publication_time = time(hour=raw_time.hour, minute=raw_time.minute)
    except ValueError:
        await message.answer(Errors.invalid_time_format)
    else:
        model = await redis.get_new_publication()
        (year, month, day) = map(int, model.raw_date.split("-"))
        local_date = TIMEZONE.localize(
            datetime(year=year, month=month, day=day, hour=publication_time.hour, minute=publication_time.minute))
        publication_date = local_date.astimezone(pytz.utc)
        model.datetime = datetime_to_unix(publication_date)
        await redis.save_new_publication(model)

        await message.edit_text(Strings.publication_text, reply_markup=NewPublicationInlineMarkups.publication_text())
        await state.set_state(NewPublicationStates.publication_text)