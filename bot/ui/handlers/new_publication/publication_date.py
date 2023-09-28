from datetime import datetime, timedelta

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from bot.data.redis.queries import RedisQueries
from bot.data.redis.models.new_publication import NewPublicationModel
from bot.ui.res.strings import Strings, Errors
from bot.ui.res.buttons import Action
from bot.ui.keyboards.inline_markups import NewPublicationInlineMarkups, MenuCallbackFactory
from bot.ui.states.state_machine import MenuNavigationStates, NewPublicationStates


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.new_publication),
    MenuNavigationStates.main_menu)
@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.schedule_next_publication),
    NewPublicationStates.schedule_publication)
async def new_publication(query: CallbackQuery, state: FSMContext, redis: RedisQueries) -> None:
    """
    Запускает цепочку "Новая публикация". Первое - это дата публикации.
    :param query:
    :param state:
    :param redis:
    :return:
    """
    await redis.save_new_publication(NewPublicationModel())

    await query.message.edit_text(Strings.publication_date, reply_markup=NewPublicationInlineMarkups.publication_date())
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
    match callback_data.action:
        case Action.today:
            raw_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).date()
        case Action.tomorrow:
            raw_date = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)).date()
        case _:
            raw_date = datetime.now().date()
    model.raw_date = str(raw_date)
    await redis.save_new_publication(model)

    await query.message.edit_text(Strings.publication_time, reply_markup=NewPublicationInlineMarkups.publication_time())
    await state.set_state(NewPublicationStates.publication_time)


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
        publication_date = datetime(year=datetime.now().year, month=raw_date.month, day=raw_date.day)
    except ValueError:
        await message.answer(Errors.invalid_date_format)
    else:
        model = await redis.get_new_publication()
        model.raw_date = str(publication_date)
        await redis.save_new_publication(model)

        await message.answer(Strings.publication_time, reply_markup=NewPublicationInlineMarkups.publication_time())
        await state.set_state(NewPublicationStates.publication_time)
