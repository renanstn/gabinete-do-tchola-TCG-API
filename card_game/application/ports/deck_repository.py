from abc import ABC, abstractmethod

from domain.card import Card


class DeckRepository(ABC):
    """Porta de saída para obtenção das cartas de um deck."""

    @abstractmethod
    def get_cards(self, deck_id: str) -> list[Card]:
        pass
