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
        id: str = None,
        description: str = None,
        image: Optional[str] = None,
    ):
        if not id:
            self.id = str(uuid.uuid4())
        self.hp = hp
        self.atk = atk
        self.name = name
        self.card_type = card_type
        self.description = description
        self.image = image
