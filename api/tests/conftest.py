import pytest
from api.game.card import Card, CardType
from api.game.game import Game
from api.game.player import Player


@pytest.fixture
def player_with_default_deck():
    deck = [
        Card(5, 5, "card A", CardType.CHARACTER),
        Card(5, 5, "card B", CardType.CHARACTER),
        Card(5, 5, "card C", CardType.CHARACTER),
        Card(5, 5, "card D", CardType.CHARACTER),
        Card(5, 5, "card E", CardType.CHARACTER),
    ]
    player = Player("Foo", deck.copy())
    return player
