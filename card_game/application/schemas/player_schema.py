from pydantic import BaseModel


class CreatePlayerSchema(BaseModel):
    name: str
    deck_id: str
