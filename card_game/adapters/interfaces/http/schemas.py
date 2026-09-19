from uuid import UUID

from pydantic import BaseModel


class CreatePlayerRequest(BaseModel):
    name: str
    deck_id: UUID
