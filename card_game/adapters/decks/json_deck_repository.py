from uuid import UUID

import json
from pathlib import Path

from application.exceptions import DeckNotFoundError
from application.ports.deck_repository import DeckRepository
from domain.card import Card, CardType, CharacterCard, ItemCard, StageCard


class JsonDeckRepository(DeckRepository):
    """Adaptador que lê definições de deck locais em JSON."""

    def __init__(self, decks_path: Path):
        self.decks_path = decks_path

    def get_cards(self, deck_id: UUID) -> list[Card]:
        for deck_path in sorted(self.decks_path.glob("*.json")):
            if not deck_path.is_file():
                continue
            definition = json.loads(deck_path.read_text(encoding="utf-8"))
            try:
                stored_id = UUID(str(definition.get("id", "")))
            except ValueError:
                continue
            if stored_id == deck_id:
                return [self._to_card(card) for card in definition["cards"]]
        raise DeckNotFoundError(f"Deck {deck_id!r} not found.")

    @staticmethod
    def _to_card(definition: dict[str, object]) -> Card:
        common = dict(
            name=str(definition["name"]),
            play_requirements=definition.get("play_requirements"),
            description=str(definition.get("description") or ""),
            image=str(definition.get("image") or "") or None,
            sound=str(definition.get("sound") or "") or None,
        )
        card_type = CardType(str(definition["card_type"]))
        if card_type == CardType.CHARACTER:
            return CharacterCard(
                hp=int(definition["hp"]), atk=int(definition["atk"]), **common
            )
        if card_type == CardType.ITEM:
            return ItemCard(
                hp_modifier=int(definition.get("hp_modifier", 0)),
                atk_modifier=int(definition.get("atk_modifier", 0)),
                deactivate=definition.get("deactivate", False),
                hp_set=(
                    int(definition["hp_set"])
                    if definition.get("hp_set") is not None
                    else None
                ),
                atk_set=(
                    int(definition["atk_set"])
                    if definition.get("atk_set") is not None
                    else None
                ),
                **common,
            )
        return StageCard(**common)
