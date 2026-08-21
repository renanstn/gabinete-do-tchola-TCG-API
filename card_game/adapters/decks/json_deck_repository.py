import json
from pathlib import Path

from application.exceptions import DeckNotFoundError
from application.ports.deck_repository import DeckRepository
from domain.card import Card, CardType


class JsonDeckRepository(DeckRepository):
    """Adaptador que lê definições de deck locais em JSON."""

    def __init__(self, decks_path: Path):
        self.decks_path = decks_path

    def get_cards(self, deck_id: str) -> list[Card]:
        deck_path = self.decks_path / f"deck_{deck_id}.json"
        if not deck_path.is_file():
            raise DeckNotFoundError(f"Deck {deck_id!r} não encontrado.")

        definition = json.loads(deck_path.read_text(encoding="utf-8"))
        return [self._to_card(card) for card in definition["cards"]]

    @staticmethod
    def _to_card(definition: dict[str, object]) -> Card:
        return Card(
            name=str(definition["name"]),
            card_type=CardType(str(definition["card_type"])),
            hp=int(definition["hp"]),
            atk=int(definition["atk"]),
            description=str(definition.get("description") or ""),
            image=str(definition.get("image") or "") or None,
        )
