import uuid
from enum import Enum
from typing import List, Optional


class CardType(Enum):
    CHARACTER = "character"
    ITEM = "item"


class Card:
    """
    Instância de uma carta. Cartas podem ser personagens ou items.
    """

    def __init__(
        self,
        hp: int,
        atk: int,
        name: str,
        card_type: CardType,
        description: str = None,
        image: Optional[str] = None,
    ):
        self.id = uuid.uuid4()
        self.hp = 5
        self.atk = 2
        self.name = name
        self.card_type = card_type
        self.description = description
        self.image = image
