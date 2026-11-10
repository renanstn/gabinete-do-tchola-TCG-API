import json

import pytest
from adapters.repositories.game_snapshot import (
    game_from_snapshot,
    game_to_snapshot,
)
from domain.card import Card, CardType
from domain.game import Game
from domain.player import Player


@pytest.fixture
def populated_game():
    def character(name):
        return Card(8, 3, name, CardType.CHARACTER)

    game = Game(
        Player("João", [character("first"), character("last")]),
        Player("B", [character("opponent")]),
    )
    player = game.player_a
    player.cards_in_hand = [character("hand")]
    player.table = [character("equipped"), character("next target")]
    player.cemetery = [character("dead")]
    player.cemetery[0].hp = -1
    item = Card(
        0,
        0,
        "item",
        CardType.ITEM,
        description="efeito",
        image="image.png",
        sound="sound.wav",
        hp_modifier=2,
        atk_modifier=-1,
        deactivate=True,
    )
    player.table[0].apply_item(item)
    player.table[0].take_damage(4)
    player.table[1].activate()
    player.has_played_card = True
    player.hp = 7
    game.active_player_id = game.player_b.id
    return game


def assert_same_card(actual, expected):
    assert vars(actual).keys() == vars(expected).keys()
    for field, value in vars(expected).items():
        if field != "items":
            assert getattr(actual, field) == value
    assert len(actual.items) == len(expected.items)
    for actual_item, expected_item in zip(actual.items, expected.items):
        assert_same_card(actual_item, expected_item)


def assert_same_game(actual, expected):
    assert actual.id == expected.id
    assert actual.active == expected.active
    assert actual.active_player_id == expected.active_player_id
    assert (actual.winner.id if actual.winner else None) == (
        expected.winner.id if expected.winner else None
    )
    for actual_player, expected_player in zip(
        actual.players, expected.players
    ):
        assert actual_player.id == expected_player.id
        assert actual_player.name == expected_player.name
        assert actual_player.hp == expected_player.hp
        assert actual_player.has_played_card == expected_player.has_played_card
        for zone in ("deck", "cards_in_hand", "table", "cemetery"):
            actual_cards = getattr(actual_player, zone)
            expected_cards = getattr(expected_player, zone)
            assert len(actual_cards) == len(expected_cards)
            for actual_card, expected_card in zip(
                actual_cards, expected_cards
            ):
                assert_same_card(actual_card, expected_card)


@pytest.mark.parametrize("finished", [False, True])
def test_round_trip_preserves_complete_game_state(populated_game, finished):
    if finished:
        populated_game.player_a.hp = 0
        populated_game.end_game()
    snapshot = json.loads(json.dumps(game_to_snapshot(populated_game)))
    restored = game_from_snapshot(snapshot)
    assert_same_game(restored, populated_game)
    if finished:
        assert restored.winner is restored.player_b
    restored.player_a.table[0].hp = 99
    assert populated_game.player_a.table[0].hp == 6


def test_restored_game_can_continue_playing(populated_game):
    restored = game_from_snapshot(game_to_snapshot(populated_game))
    restored.end_turn(restored.player_b.id)
    assert restored.active_player_id == restored.player_a.id
    assert not restored.player_a.has_played_card
    assert restored.player_a.cards_in_hand[-1].name == "last"


def test_unknown_snapshot_version_is_rejected(populated_game):
    snapshot = game_to_snapshot(populated_game)
    snapshot["version"] = 999
    with pytest.raises(ValueError, match="version"):
        game_from_snapshot(snapshot)
