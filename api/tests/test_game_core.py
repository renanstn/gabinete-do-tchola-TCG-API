from api.game.card import Card, CardType
from api.game.game import Game
from api.game.player import Player


def test_new_game():
    """
    Dado 2 players e um deck default, deve ser possível iniciar um game.
    """
    deck = [
        Card(5, 5, "card A", CardType.CHARACTER),
        Card(5, 5, "card B", CardType.CHARACTER),
        Card(5, 5, "card C", CardType.CHARACTER),
        Card(5, 5, "card D", CardType.CHARACTER),
        Card(5, 5, "card E", CardType.CHARACTER),
    ]
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)

    game.setup_game()

    assert game.turn == True
    assert len(player_a.cards_in_hand) == 5
    assert len(player_b.cards_in_hand) == 5
