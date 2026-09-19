import logging
import uuid
from enum import Enum


logger = logging.getLogger(__name__)


class CardType(Enum):
    CHARACTER = "character"
    ITEM = "item"
    STAGE = "stage"


class Card:
    """
    Instância de uma carta. Cartas podem ser personagens, intens ou cenários.
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
        sound: str | None = None,
        hp_modifier: int = 0,
        atk_modifier: int = 0,
        deactivate: bool = False,
    ):
        self.id: str = id or str(uuid.uuid4())
        self.hp: int = hp
        self.initial_hp: int = hp
        self.atk: int = atk
        self.name: str = name
        self.card_type: CardType = card_type
        self.description: str | None = description
        self.image: str | None = image
        self.sound: str | None = sound
        self.can_attack: bool = False
        self.items: list[Card] = []
        self.hp_modifier = hp_modifier
        self.atk_modifier = atk_modifier
        self.deactivate = deactivate

    def take_damage(self, damage: int) -> None:
        self.hp -= damage

    def is_dead(self) -> bool:
        return self.hp <= 0

    def is_hurted(self) -> bool:
        return self.hp != self.initial_hp

    def activate(self) -> None:
        self.can_attack = True

    def has_items(self) -> bool:
        return bool(self.items)

    def apply_item(self, item: "Card") -> None:
        self.hp += item.hp_modifier
        self.initial_hp += item.hp_modifier
        self.atk = max(0, self.atk + item.atk_modifier)
        if item.deactivate:
            self.can_attack = False
        self.items.append(item)
