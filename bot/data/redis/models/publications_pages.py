from enum import Enum
from typing import TypeAlias

from pydantic import BaseModel

from bot.data.redis.models.publications import PublicationModel


PublicationWeekMap: TypeAlias = dict[str, list[PublicationModel]]
PublicationMonthMap: TypeAlias = dict[str, PublicationWeekMap]


class TypesOfPages(int, Enum):
    upcoming_publications = 0
    overdue_publications = 1
    published = 2


class PagesConfigModel(BaseModel):
    current_page_index: int = 0
    current_page_num: int = 1
    max_pages: int
    page_type: TypesOfPages


class UpcomingPublicationsPagesModel(BaseModel):
    period_map: PublicationMonthMap
    selected_month: str = ""
    selected_week: str = ""


class ArchivedPublicationsPagesModel(BaseModel):
    publications: tuple[PublicationModel, ...]
