from pydantic import BaseModel


class CreatePlayerSchema(BaseModel):
    """
    This schema is used to validate the input data when creating a new player.
    """

    name: str
    deck_id: str
