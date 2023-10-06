from aiogram import Router
from aiogram.filters import Command, StateFilter
from magic_filter import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.ui.res.buttons import Action
from bot.ui.res.strings import Strings
from bot.ui.keyboards.inline_markups import MenuCallbackFactory, MainMenuMarkups
from bot.ui.states.state_machine import MenuNavigationStates, NewPublicationStates, ScheduledPublicationsStates


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await message.answer(Strings.main_menu, reply_markup=MainMenuMarkups.main_menu())
    await state.set_state(MenuNavigationStates.main_menu)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back_to_main_menu),
    StateFilter(NewPublicationStates, ScheduledPublicationsStates))
async def back_to_main_menu_button(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text(Strings.main_menu, reply_markup=MainMenuMarkups.main_menu())
    await state.set_state(MenuNavigationStates.main_menu)

