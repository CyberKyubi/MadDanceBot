from aiogram.fsm.state import StatesGroup, State


class MenuNavigationStates(StatesGroup):
    main_menu = State()


class NewPublicationStates(StatesGroup):
    publication_date = State()
    publication_time = State()
    publication_text = State()
    editing_publication_text = State()
