import json

import pytest
from adapters.repositories.game_snapshot import (
    game_from_snapshot,
    game_to_snapshot,
)
from domain.card import CharacterCard, ItemCard, StageCard
from domain.game import Game
from domain.player import Player


@pytest.fixture
def populated_game():
    def character(name):
        return CharacterCard(8, 3, name)

    game = Game(
        Player("João", [character("first"), character("last")]),
        Player("B", [character("opponent")]),
    )
    player = game.player_a
    player.cards_in_hand = [character("hand")]
    player.table = [character("equipped"), character("next target")]
    player.cemetery = [character("dead")]
    player.cemetery[0].hp = -1
    item = ItemCard(
        "item",
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
    assert type(actual) is type(expected)
    assert vars(actual).keys() == vars(expected).keys()
    for field, value in vars(expected).items():
        if field != "items":
            assert getattr(actual, field) == value
    if not isinstance(expected, CharacterCard):
        return
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
    for actual_player, expected_player in zip(actual.players, expected.players):
        assert actual_player.id == expected_player.id
        assert actual_player.name == expected_player.name
        assert actual_player.hp == expected_player.hp
        assert actual_player.has_played_card == expected_player.has_played_card
        for zone in ("deck", "cards_in_hand", "table", "cemetery"):
            actual_cards = getattr(actual_player, zone)
            expected_cards = getattr(expected_player, zone)
            assert len(actual_cards) == len(expected_cards)
            for actual_card, expected_card in zip(actual_cards, expected_cards):
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


def test_absolute_effects_survive_persistence_without_being_reapplied(populated_game):
    target = populated_game.player_a.table[0]
    target.apply_item(ItemCard("Set", hp_set=1, atk_set=5))
    target.take_damage(1)
    restored = game_from_snapshot(game_to_snapshot(populated_game))
    assert_same_game(restored, populated_game)
    assert restored.player_a.table[0].hp == 0
    effect = restored.player_a.table[0].items[-1]
    assert (effect.hp_set, effect.atk_set) == (1, 5)


def test_old_snapshots_without_absolute_effects_are_supported(populated_game):
    snapshot = game_to_snapshot(populated_game)

    def strip_new_fields(card):
        card.pop("hp_set", None)
        card.pop("atk_set", None)
        for item in card.get("items", []):
            strip_new_fields(item)

    for player in snapshot["players"]:
        for zone in ("deck", "cards_in_hand", "table", "cemetery"):
            for card in player[zone]:
                strip_new_fields(card)
    assert_same_game(game_from_snapshot(snapshot), populated_game)


def test_scenarios_and_unequipped_items_survive_round_trip(populated_game):
    populated_game.player_a.cards_in_hand.extend(
        [
            StageCard("Forest"),
            ItemCard("Sword", atk_modifier=2),
        ]
    )
    snapshot = game_to_snapshot(populated_game)
    assert snapshot["version"] == 3
    restored = game_from_snapshot(json.loads(json.dumps(snapshot)))
    assert_same_game(restored, populated_game)


def test_legacy_snapshot_with_fields_from_all_card_types(populated_game):
    snapshot = game_to_snapshot(populated_game)
    snapshot["version"] = 1

    def add_legacy_fields(card):
        defaults = dict(
            hp=0,
            initial_hp=0,
            atk=0,
            can_attack=False,
            items=[],
            hp_modifier=0,
            atk_modifier=0,
            deactivate=False,
            hp_set=None,
            atk_set=None,
        )
        for key, value in defaults.items():
            card.setdefault(key, value)
        for item in card["items"]:
            add_legacy_fields(item)

    for player in snapshot["players"]:
        for zone in ("deck", "cards_in_hand", "table", "cemetery"):
            for card in player[zone]:
                add_legacy_fields(card)
    assert_same_game(game_from_snapshot(snapshot), populated_game)


def test_round_and_requirements_survive_snapshot(populated_game):
    populated_game.round_number = 8
    populated_game.active_stage = StageCard("Forest")
    populated_game.player_a.cards_in_hand[0].play_requirements = {
        "active_stage": {"name": "Forest"},
        "card_on_table": {"id": populated_game.player_a.table[0].id},
    }
    restored = game_from_snapshot(
        json.loads(json.dumps(game_to_snapshot(populated_game)))
    )
    assert restored.round_number == 8
    assert_same_card(restored.active_stage, populated_game.active_stage)
    assert_same_game(restored, populated_game)


@pytest.mark.parametrize("version", [1, 2])
def test_legacy_snapshots_default_to_first_round(populated_game, version):
    snapshot = game_to_snapshot(populated_game)
    snapshot["version"] = version
    snapshot.pop("round_number")
    snapshot.pop("active_stage")
    for player in snapshot["players"]:
        for zone in ("deck", "cards_in_hand", "table", "cemetery"):
            for card in player[zone]:
                card.pop("play_requirements", None)
    restored = game_from_snapshot(snapshot)
    assert restored.round_number == 1
    assert restored.active_stage is None
    assert_same_game(restored, populated_game)
