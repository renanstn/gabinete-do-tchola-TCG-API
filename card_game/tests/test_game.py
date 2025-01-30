import pytest

from card_game.domain.card import Card, CardType
from card_game.domain.game import Game
from card_game.domain.player import Player


@pytest.fixture
def setup_players():
    deck_a = [
        Card(hp=5, atk=3, name="Card A1", card_type=CardType.CHARACTER)
        for _ in range(10)
    ]
    deck_b = [
        Card(hp=4, atk=2, name="Card B1", card_type=CardType.CHARACTER)
        for _ in range(10)
    ]
    player_a = Player(name="Player A", deck=deck_a)
    player_b = Player(name="Player B", deck=deck_b)
    return player_a, player_b


@pytest.fixture
def setup_game(setup_players):
    player_a, player_b = setup_players
    game = Game(player_a=player_a, player_b=player_b)
    return game


def test_setup_game(setup_game):
    game = setup_game
    game.setup_game()
    assert len(game.player_a.cards_in_hand) == 5
    assert len(game.player_b.cards_in_hand) == 5
    assert len(game.player_a.deck) == 5
    assert len(game.player_b.deck) == 5


def test_switch_turn(setup_game):
    game = setup_game
    initial_turn = game.turn
    game.switch_turn()
    assert game.turn != initial_turn


def test_get_active_player_and_opponent(setup_game):
    game = setup_game
    active_player, opponent = game.get_active_player_and_opponent()
    assert active_player == game.player_a
    assert opponent == game.player_b
    game.switch_turn()
    active_player, opponent = game.get_active_player_and_opponent()
    assert active_player == game.player_b
    assert opponent == game.player_a


def test_end_play(setup_game):
    game = setup_game
    game.setup_game()
    active_player, opponent = game.get_active_player_and_opponent()
    active_player.table.append(active_player.cards_in_hand.pop())
    game.end_play()
    assert game.turn == False
    assert opponent.is_alive()


def test_compute_battle(setup_game):
    game = setup_game
    game.setup_game()
    active_player, opponent = game.get_active_player_and_opponent()
    active_player.table.append(active_player.cards_in_hand.pop())
    opponent.table.append(opponent.cards_in_hand.pop())
    game.compute_battle(active_player, opponent)
    assert opponent.hp == 10


def test_end_game(setup_game):
    game = setup_game
    game.setup_game()
    game.player_b.hp = 0
    game.end_game()
    assert game.winner == game.player_a
    assert game.active == False
