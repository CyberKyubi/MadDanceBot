from datetime import datetime

from pydantic import BaseModel


class PublicationModel(BaseModel):
    publication_id: int
    publication_title: str
    publication_text: str
    publication_at: int
    is_published: bool


class ScheduledPublicationModel(BaseModel):
    publication_id: int
    publication_text: str
    publication_at: datetime


class CategorizedPublicationsModel(BaseModel):
    upcoming: tuple[PublicationModel] | None
    overdue: tuple[PublicationModel] | None
