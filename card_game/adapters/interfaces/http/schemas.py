from pydantic import BaseModel


class CreatePlayerRequest(BaseModel):
    name: str
    deck_id: str
