import pytest

from domain.card import Card, CardType
from domain.game import Game
from domain.player import Player


@pytest.fixture
def deck():
    deck = [
        Card(hp=5, atk=5, name="card A", card_type=CardType.CHARACTER, id="1"),
        Card(hp=5, atk=5, name="card A", card_type=CardType.CHARACTER, id="2"),
        Card(hp=5, atk=5, name="card A", card_type=CardType.CHARACTER, id="3"),
        Card(hp=5, atk=5, name="card A", card_type=CardType.CHARACTER, id="4"),
        Card(hp=5, atk=5, name="card A", card_type=CardType.CHARACTER, id="5"),
    ]
    return deck
