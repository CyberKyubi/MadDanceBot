from aiogram import Router


def setup_routers() -> Router:
    from . import main_menu
    from .new_publication import (
        new_publication_common,
        publication_date,
        publication_time,
        publication_text)
    from .scheduled_publications import (
        scheduled_publications_common,
        scheduled_publications,
        upcoming_publications,
        overdue_publications)
    from .publications_pages import publication_page

    router = Router()

    router.include_router(main_menu.router)
    router.include_router(new_publication_common.router)
    router.include_router(publication_date.router)
    router.include_router(publication_time.router)
    router.include_router(publication_text.router)

    router.include_router(scheduled_publications_common.router)
    router.include_router(scheduled_publications.router)
    router.include_router(upcoming_publications.router)
    router.include_router(overdue_publications.router)

    router.include_router(publication_page.router)

    return router
