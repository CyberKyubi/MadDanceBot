from datetime import datetime, time

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from bot.ui.res.strings import Strings, Errors
from bot.ui.res.buttons import Action, Value
from bot.ui.keyboards.inline_markups import NewPublicationInlineMarkups, MenuCallbackFactory
from bot.ui.states.state_machine import MenuNavigationStates, NewPublicationStates


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(
        (F.action == Action.now) | (F.action == Action.twelve_clock) | (F.action == Action.fifteen_clock) |
        (F.action == Action.eighteen_clock) | (F.action == Action.five_clock)
    ),
    NewPublicationStates.publication_time)
async def publication_time_hot_buttons(query: CallbackQuery, callback_data: MenuCallbackFactory, state: FSMContext) -> None:
    """
    Обрабатывает "горячие" кнопки времени публикации.
    :param query:
    :param callback_data:
    :param state:
    :return:
    """
    if callback_data.value == Value.now:
        print("now")
    else:
        hot_time = callback_data.value
        await publication_time_entry(query.message, state, hot_time)


@router.message(NewPublicationStates.publication_time)
async def publication_time_entry(message: Message, state: FSMContext, hot_time: str = None) -> None:
    """
    Проверяет формат введенного времени публикации.
    :param message:
    :param state:
    :param hot_time:
    :return:
    """
    try:
        raw_time = datetime.strptime(message.text if not hot_time else hot_time, "%H.%M")
        publication_time = time(hour=raw_time.hour, minute=raw_time.minute)
    except ValueError:
        await message.answer(Errors.invalid_time_format)
    else:
        # todo save

        await message.answer(Strings.publication_text)
        await state.set_state(NewPublicationStates.publication_text)