"""Card identities and the rules specific to each card category."""

import uuid
from abc import ABC, abstractmethod
from enum import Enum


class CardType(Enum):
    CHARACTER = "character"
    ITEM = "item"
    STAGE = "stage"


class Card(ABC):
    def __init__(
        self,
        name: str,
        id: str | None = None,
        description: str | None = None,
        image: str | None = None,
        sound: str | None = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.image = image
        self.sound = sound

    @property
    @abstractmethod
    def card_type(self) -> CardType:
        """The category is fixed by the concrete card class."""


class ItemCard(Card):
    def __init__(
        self,
        name: str,
        *,
        hp_modifier: int = 0,
        atk_modifier: int = 0,
        deactivate: bool = False,
        hp_set: int | None = None,
        atk_set: int | None = None,
        id: str | None = None,
        description: str | None = None,
        image: str | None = None,
        sound: str | None = None
    ):
        super().__init__(name, id, description, image, sound)
        self.hp_modifier = hp_modifier
        self.atk_modifier = atk_modifier
        self.deactivate = deactivate
        self.hp_set = hp_set
        self.atk_set = atk_set
        self.validate_item_effects()

    @property
    def card_type(self) -> CardType:
        return CardType.ITEM

    def validate_item_effects(self) -> None:
        if (self.hp_set is not None or self.atk_set is not None) and (
            self.hp_modifier != 0 or self.atk_modifier != 0
        ):
            raise ValueError("Items cannot combine *_set and *_modifier effects.")


class StageCard(Card):
    """Scenario identity; playing scenarios is not implemented yet."""

    @property
    def card_type(self) -> CardType:
        return CardType.STAGE


class CharacterCard(Card):
    def __init__(
        self,
        hp: int,
        atk: int,
        name: str,
        *,
        id: str | None = None,
        description: str | None = None,
        image: str | None = None,
        sound: str | None = None
    ):
        super().__init__(name, id, description, image, sound)
        self.hp = hp
        self.initial_hp = hp
        self.atk = atk
        self.can_attack = False
        self.items: list[ItemCard] = []

    @property
    def card_type(self) -> CardType:
        return CardType.CHARACTER

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

    def apply_item(self, item: "ItemCard") -> None:
        if not isinstance(item, ItemCard):
            raise TypeError("Only items can be applied to a character.")
        item.validate_item_effects()
        if item.hp_set is not None:
            self.hp = item.hp_set
        if item.atk_set is not None:
            self.atk = item.atk_set
        self.hp += item.hp_modifier
        self.initial_hp += item.hp_modifier
        self.atk = max(0, self.atk + item.atk_modifier)
        if item.deactivate:
            self.can_attack = False
        self.items.append(item)
