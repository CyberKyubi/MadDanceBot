from pydantic import BaseModel


class NewPublicationModel(BaseModel):
    date: int = 0
    time: int = 0
    text: str = ""

    message_id: int = 0
