from pydantic import BaseModel


class NewPublicationModel(BaseModel):
    raw_date: str = ""
    unix_timestamp: int = 0
    is_now: bool = False
    title: str = ""
    text: str = ""

    message_id: int = 0
