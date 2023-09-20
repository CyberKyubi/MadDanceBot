from aiogram import Router


def setup_routers() -> Router:
    from . import main_menu
    from .new_publication import publication_date, publication_time

    router = Router()
    router.include_router(main_menu.router)
    router.include_router(publication_date.router)
    router.include_router(publication_time.router)

    return router
