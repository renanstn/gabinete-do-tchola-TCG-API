from uuid import UUID

import json
from pathlib import Path

from application.exceptions import DeckNotFoundError
from application.ports.deck_repository import DeckRepository
from domain.card import Card, CardType


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
        return Card(
            name=str(definition["name"]),
            card_type=CardType(str(definition["card_type"])),
            hp=int(definition.get("hp", 0)),
            atk=int(definition.get("atk", 0)),
            hp_modifier=int(definition.get("hp_modifier", 0)),
            atk_modifier=int(definition.get("atk_modifier", 0)),
            deactivate=definition.get("deactivate", False),
            description=str(definition.get("description") or ""),
            image=str(definition.get("image") or "") or None,
        )
