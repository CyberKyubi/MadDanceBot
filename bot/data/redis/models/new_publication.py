from pydantic import BaseModel


class NewPublicationModel(BaseModel):
    raw_date: str = 0
    datetime: int = 0
    text: str = ""

    message_id: int = 0
