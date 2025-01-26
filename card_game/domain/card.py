import uuid
from enum import Enum
from typing import Optional


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
        self.id = id
        if not self.id:
            self.id = str(uuid.uuid4())
        self.hp = hp
        self.atk = atk
        self.name = name
        self.card_type = card_type
        self.description = description
        self.image = image
        self.can_attack = False
        self.items = []  # List of items IDs

    def take_damage(self, damage: int):
        self.hp -= damage

    def is_dead(self) -> bool:
        return self.hp <= 0

    def activate(self):
        self.can_attack = True

    def has_items(self) -> bool:
        return bool(self.items)
