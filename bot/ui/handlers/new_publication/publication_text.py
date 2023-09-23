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


@router.message(NewPublicationStates.publication_text)
async def publication_text_entry(message: Message, state: FSMContext) -> None:
    publication_text = message.text
    # todo save

    await message.answer(
        Strings.editing_publication_text,
        reply_markup=NewPublicationInlineMarkups.editing_publication_text())
    await state.set_state(NewPublicationStates.editing_publication_text)


@router.edited_message(NewPublicationStates.editing_publication_text)
async def editing_publication_text(message: Message, state: FSMContext) -> None:
    if message.message_id != 1:
        return

    print(message.text)
