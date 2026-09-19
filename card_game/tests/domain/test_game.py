import pytest

from domain.card import Card, CardType
from domain.game import Game
from domain.player import Player


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
    assert len(game.player_a.cards_in_hand) == 6
    assert len(game.player_b.cards_in_hand) == 5
    assert len(game.player_a.deck) == 4
    assert len(game.player_b.deck) == 5


def test_switch_turn(setup_game):
    game = setup_game
    initial_active_player_id = game.active_player_id
    game.switch_turn()
    assert game.active_player_id != initial_active_player_id
    assert game.active_player_id == game.player_b.id


def test_get_active_player_and_opponent(setup_game):
    game = setup_game
    active_player, opponent = game.get_active_player_and_opponent()
    assert active_player == game.player_a
    assert opponent == game.player_b
    game.switch_turn()
    active_player, opponent = game.get_active_player_and_opponent()
    assert active_player == game.player_b
    assert opponent == game.player_a


def test_end_turn(setup_game):
    game = setup_game
    game.setup_game()
    active_player, opponent = game.get_active_player_and_opponent()
    active_player.table.append(active_player.cards_in_hand.pop())
    game.end_turn(game.active_player_id)
    assert game.active_player_id == game.player_b.id
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


def test_each_turn_draws_only_for_the_incoming_player(setup_game):
    game = setup_game
    game.setup_game()
    game.end_turn(game.active_player_id)
    assert len(game.player_a.cards_in_hand) == 6
    assert len(game.player_b.cards_in_hand) == 6
    assert len(game.player_b.deck) == 4
    game.end_turn(game.active_player_id)
    assert len(game.player_a.cards_in_hand) == 7
    assert len(game.player_a.deck) == 3
    assert len(game.player_b.cards_in_hand) == 6


def test_empty_deck_does_not_prevent_turns(setup_game):
    game = setup_game
    game.setup_game()
    for _ in range(20):
        game.end_turn(game.active_player_id)
    assert game.active
    for player in game.players:
        assert len(player.cards_in_hand) == 10
        assert player.deck == []
        assert player.hp == 10


def test_lethal_battle_does_not_start_another_turn(setup_game):
    game = setup_game
    game.setup_game()
    attacker = game.player_a.cards_in_hand.pop()
    attacker.activate()
    game.player_a.table.append(attacker)
    game.player_b.hp = attacker.atk
    game.end_turn(game.active_player_id)
    assert not game.active
    assert game.winner == game.player_a
    assert len(game.player_b.cards_in_hand) == 5
    assert len(game.player_b.deck) == 5


@pytest.mark.parametrize("action", ["play_card", "end_turn"])
@pytest.mark.parametrize("invalid_state", ["finished", "opponent", "outsider"])
def test_invalid_moves_leave_game_unchanged(setup_game, action, invalid_state):
    from copy import deepcopy
    from uuid import uuid4

    from domain.exceptions import InvalidMoveError

    game = setup_game
    game.setup_game()
    player_id = game.active_player_id
    if invalid_state == "finished":
        game.player_b.hp = 0
        game.end_game()
        message = "The game has already ended"
    else:
        player_id = game.player_b.id if invalid_state == "opponent" else uuid4()
        message = "It is not this player's turn"
    before = deepcopy(game)

    with pytest.raises(InvalidMoveError, match=message):
        if action == "play_card":
            game.play_card(player_id, game.player_a.cards_in_hand[0].id)
        else:
            game.end_turn(player_id)

    assert game.active == before.active
    assert game.active_player_id == before.active_player_id
    assert (game.winner.id if game.winner else None) == (
        before.winner.id if before.winner else None
    )
    for player, original in zip(game.players, before.players):
        assert player.hp == original.hp
        for zone in ("deck", "cards_in_hand", "table", "cemetery"):
            assert [vars(card) for card in getattr(player, zone)] == [
                vars(card) for card in getattr(original, zone)
            ]


def test_game_play_card_checks_player_rules(setup_game):
    from domain.exceptions import InvalidMoveError

    game = setup_game
    game.setup_game()
    player = game.player_a
    card = player.cards_in_hand[0]
    game.play_card(player.id, card.id)
    assert player.table == [card]
    assert card not in player.cards_in_hand
    with pytest.raises(InvalidMoveError, match="already played a card"):
        game.play_card(player.id, player.cards_in_hand[0].id)
    assert player.table == [card]
