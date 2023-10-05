from pydantic import BaseModel


class NewPublicationModel(BaseModel):
    publication_title: str = ""
    publication_text: str = ""
    raw_date: str = ""
    publication_at: int = 0
    is_now: bool = False

    message_id: int = 0
