from aiogram.fsm.state import StatesGroup, State


class MenuNavigationStates(StatesGroup):
    main_menu = State()


class NewPublicationStates(StatesGroup):
    publication_date = State()
    publication_time = State()
    publication_title = State()
    publication_text = State()
    editing_publication_text = State()
    schedule_publication = State()


class ScheduledPublicationsStates(StatesGroup):
    overdue_and_upcoming_publications = State()
    month_selection = State()
    week_selection = State()


class PublicationsPagesStates(StatesGroup):
    publication_page = State()