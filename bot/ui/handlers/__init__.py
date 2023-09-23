from aiogram import Router


def setup_routers() -> Router:
    from . import main_menu
    from .new_publication import new_publication_common, publication_date, publication_time, publication_text

    router = Router()

    router.include_router(main_menu.router)
    router.include_router(new_publication_common.router)
    router.include_router(publication_date.router)
    router.include_router(publication_time.router)
    router.include_router(publication_text.router)

    return router
