import uuid
from enum import Enum

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
        id: str | None = None,
        description: str | None = None,
        image: str | None = None,
    ):
        self.id: str = id or str(uuid.uuid4())
        self.hp: int = hp
        self.atk: int = atk
        self.name: str = name
        self.card_type: CardType = card_type
        self.description: str | None = description
        self.image: str | None = image
        self.can_attack: bool = False
        self.items: list[str] = []  # IDs dos itens aplicados

    def take_damage(self, damage: int) -> None:
        self.hp -= damage

    def is_dead(self) -> bool:
        return self.hp <= 0

    def activate(self) -> None:
        self.can_attack = True

    def has_items(self) -> bool:
        return bool(self.items)
