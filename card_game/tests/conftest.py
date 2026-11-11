import pytest

from domain.card import CharacterCard
from domain.game import Game
from domain.player import Player


@pytest.fixture
def deck():
    deck = [
        CharacterCard(hp=5, atk=5, name="card A", id="1"),
        CharacterCard(hp=5, atk=5, name="card A", id="2"),
        CharacterCard(hp=5, atk=5, name="card A", id="3"),
        CharacterCard(hp=5, atk=5, name="card A", id="4"),
        CharacterCard(hp=5, atk=5, name="card A", id="5"),
    ]
    return deck
