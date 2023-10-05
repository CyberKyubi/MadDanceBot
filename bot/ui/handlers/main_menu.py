from aiogram import Router
from aiogram.filters import Command, StateFilter
from magic_filter import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from bot.data.db.queries import select_upcoming_publications, select_overdue_unpublished_publications
from bot.ui.res.buttons import Action
from bot.ui.res.strings import Strings
from bot.ui.keyboards.inline_markups import MenuCallbackFactory, BaseInlineMarkups
from bot.ui.states.state_machine import MenuNavigationStates, NewPublicationStates
from bot.job_scheduler.jobs import send_publication_to_channel
from bot.mics.text_formatting import generate_text_upcoming_publications


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db) -> None:
    # upcoming_publications = await select_upcoming_publications(db)
    # overdue_publications = await retrieve_overdue_unpublished_publications(db)
    #
    # text = Strings.no_upcoming_publications
    # if upcoming_publications:
    #     generate_text_upcoming_publications(upcoming_publications)
    await message.answer(Strings.main_menu, reply_markup=BaseInlineMarkups.main_menu())
    await state.set_state(MenuNavigationStates.main_menu)


@router.callback_query(
    MenuCallbackFactory.filter(F.action == Action.back_to_main_menu),
    StateFilter(NewPublicationStates))
async def back_to_main_menu_button(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_text(Strings.main_menu, reply_markup=BaseInlineMarkups.main_menu())
    await state.set_state(MenuNavigationStates.main_menu)

