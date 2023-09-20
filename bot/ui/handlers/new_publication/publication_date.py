from datetime import datetime, date

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from ui.res.strings import Strings, Errors
from ui.res.buttons import Action
from ui.keyboards.inline_markups import NewPublicationInlineMarkups, MenuCallbackFactory
from ui.states.state_machine import MenuNavigationStates, NewPublicationStates


router = Router()


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.new_publication),
    MenuNavigationStates.main_menu)
async def new_publication(query: CallbackQuery, state: FSMContext) -> None:
    """
    Запускает цепочку "Новая публикация". Первое - это дата публикации.
    :param query:
    :param state:
    :return:
    """
    await query.message.edit_text(Strings.publication_date, reply_markup=NewPublicationInlineMarkups.publication_date())
    await state.set_state(NewPublicationStates.publication_date)


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
    MenuCallbackFactory.filter((F.action == Action.today) | (F.action == Action.tomorrow)),
    NewPublicationStates.publication_date)
async def date_hot_buttons(query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает "горячие" кнопки даты публикации.
    :param query:
    :param state:
    :return:
    """
    # todo: save

    await query.message.edit_text(Strings.publication_time, reply_markup=NewPublicationInlineMarkups.publication_time())
    await state.set_state(NewPublicationStates.publication_time)


@router.message(NewPublicationStates.publication_date)
async def date_entry(message: Message, state: FSMContext) -> None:
    """
    Проверяет формат введенной даты публикации.
    :param message:
    :param state:
    :return:
    """
    try:
        raw_date = datetime.strptime(message.text, "%d.%m")
        publication_date = date(year=datetime.now().year, month=raw_date.month, day=raw_date.day)
    except ValueError:
        await message.answer(Errors.invalid_date_format)
    else:
        # todo: save

        await message.answer(Strings.publication_time, reply_markup=NewPublicationInlineMarkups.publication_time())
        await state.set_state(NewPublicationStates.publication_time)
