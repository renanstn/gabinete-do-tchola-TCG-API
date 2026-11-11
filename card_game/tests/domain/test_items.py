import pytest

from domain.card import CharacterCard, ItemCard, StageCard
from domain.exceptions import InvalidMoveError
from domain.game import Game
from domain.player import Player


def character():
    card = CharacterCard(hp=5, atk=3, name="Character")
    card.activate()
    return card


def item(**effects):
    return ItemCard(name="Item", **effects)


@pytest.fixture
def game():
    return Game(Player("Alice", []), Player("Bob", []))


@pytest.mark.parametrize("owner_index", [0, 1])
@pytest.mark.parametrize(
    "effects,hp,atk",
    [
        ({"hp_modifier": 3}, 8, 3),
        ({"hp_modifier": -2}, 3, 3),
        ({"atk_modifier": 2}, 5, 5),
        ({"atk_modifier": -2}, 5, 1),
        ({"atk_modifier": -10}, 5, 0),
        ({"hp_modifier": 1, "atk_modifier": 2}, 6, 5),
        ({"hp_set": 1}, 1, 3),
        ({"hp_set": 9}, 9, 3),
        ({"atk_set": 5}, 5, 5),
        ({"atk_set": 0}, 5, 0),
        ({"atk_set": -2}, 5, 0),
        ({"hp_set": 1, "atk_set": 5}, 1, 5),
    ],
)
def test_apply_item_to_either_player(game, owner_index, effects, hp, atk):
    target = character()
    game.players[owner_index].table.append(target)
    equipment = item(**effects)
    game.player_a.cards_in_hand.append(equipment)
    game.play_card(game.player_a.id, equipment.id, target.id)
    assert (target.hp, target.atk) == (hp, atk)
    assert target.items == [equipment]
    assert not game.player_a.cards_in_hand
    assert game.player_a.has_played_card


@pytest.mark.parametrize("owner_index", [0, 1])
def test_deactivation_skips_next_owner_battle_and_allows_play(game, owner_index):
    owner = game.players[owner_index]
    target = character()
    owner.table.append(target)
    equipment = item(deactivate=True)
    game.player_a.cards_in_hand.append(equipment)
    game.play_card(game.player_a.id, equipment.id, target.id)
    assert not target.can_attack
    if owner_index == 1:
        game.end_turn(game.player_a.id)
        assert not target.can_attack
        assert owner.can_play_card()
    opponent = game.players[1 - owner_index]
    game.end_turn(owner.id)
    assert opponent.hp == 10
    assert target.can_attack
    game.end_turn(opponent.id)
    game.end_turn(owner.id)
    assert opponent.hp == 7


def test_lethal_item_and_turn_limit(game):
    target = character()
    game.player_b.table.append(target)
    poison = item(hp_modifier=-5)
    second = character()
    game.player_a.cards_in_hand = [poison, second]
    game.play_card(game.player_a.id, poison.id, target.id)
    assert not game.player_b.table
    assert game.player_b.cemetery == [target]
    assert target.items == [poison]
    with pytest.raises(InvalidMoveError, match="already played"):
        game.play_card(game.player_a.id, second.id)


def test_item_allowed_on_full_table_and_stacks(game):
    game.player_b.hp = 100
    game.player_a.table = [character() for _ in range(5)]
    target = game.player_a.table[0]
    for _ in range(2):
        equipment = item(hp_modifier=2)
        game.player_a.cards_in_hand.append(equipment)
        game.play_card(game.player_a.id, equipment.id, target.id)
        game.end_turn(game.player_a.id)
        game.end_turn(game.player_b.id)
    assert target.hp == 9
    assert len(target.items) == 2


@pytest.mark.parametrize(
    "target_zone", ["missing", "hand", "cemetery", "item", "stage"]
)
def test_invalid_target_is_atomic(game, target_zone):
    equipment = item(hp_modifier=3)
    target = character()
    game.player_a.cards_in_hand.append(equipment)
    if target_zone == "hand":
        game.player_b.cards_in_hand.append(target)
    elif target_zone == "cemetery":
        game.player_b.cemetery.append(target)
    elif target_zone in ("item", "stage"):
        target = (
            ItemCard("Invalid target")
            if target_zone == "item"
            else StageCard("Invalid target")
        )
        game.player_b.table.append(target)
    with pytest.raises(InvalidMoveError, match="character target"):
        game.play_card(game.player_a.id, equipment.id, target.id)
    assert game.player_a.cards_in_hand == [equipment]
    assert not game.player_a.has_played_card
    if isinstance(target, CharacterCard):
        assert target.hp == 5
        assert not target.items


def test_item_requires_target_and_respects_turn_and_game_state(game):
    equipment = item(deactivate=True)
    game.player_a.cards_in_hand.append(equipment)
    for player_id, active in [
        (game.player_b.id, True),
        (game.player_a.id, False),
        (game.player_a.id, True),
    ]:
        game.active = active
        with pytest.raises(InvalidMoveError):
            game.play_card(player_id, equipment.id)
    assert game.player_a.cards_in_hand == [equipment]


def test_character_then_item_rejected(game):
    target, equipment = character(), item(atk_modifier=1)
    game.player_a.cards_in_hand = [target, equipment]
    game.play_card(game.player_a.id, target.id)
    with pytest.raises(InvalidMoveError, match="already played"):
        game.play_card(game.player_a.id, equipment.id, target.id)
    assert target.atk == 3


def test_set_hp_changes_current_life_without_resetting_initial_life(game):
    target = character()
    target.take_damage(2)
    game.player_b.table.append(target)
    equipment = item(hp_set=1)
    game.player_a.cards_in_hand.append(equipment)
    game.play_card(game.player_a.id, equipment.id, target.id)
    assert target.hp == 1
    assert target.initial_hp == 5
    assert target.is_hurted()
    target.apply_item(item(hp_modifier=3))
    assert (target.hp, target.initial_hp) == (4, 8)


@pytest.mark.parametrize("hp", [0, -1])
def test_set_hp_can_kill_target(game, hp):
    target = character()
    game.player_b.table.append(target)
    equipment = item(hp_set=hp)
    game.player_a.cards_in_hand.append(equipment)
    game.play_card(game.player_a.id, equipment.id, target.id)
    assert not game.player_b.table
    assert game.player_b.cemetery == [target]
    assert target.items == [equipment]


def test_set_replaces_previous_effects_and_later_modifiers_still_apply():
    target = character()
    target.apply_item(item(hp_modifier=3, atk_modifier=2))
    target.apply_item(item(hp_set=1, atk_set=5))
    assert (target.hp, target.atk) == (1, 5)
    target.apply_item(item(hp_modifier=3, atk_modifier=2))
    assert (target.hp, target.atk) == (4, 7)


@pytest.mark.parametrize("set_field", ["hp_set", "atk_set"])
@pytest.mark.parametrize("set_value", [0, 1])
@pytest.mark.parametrize("modifier_field", ["hp_modifier", "atk_modifier"])
@pytest.mark.parametrize("modifier_value", [-2, 3])
def test_item_rejects_mixed_effect_modes(
    set_field, set_value, modifier_field, modifier_value
):
    with pytest.raises(ValueError, match="cannot combine"):
        item(**{set_field: set_value, modifier_field: modifier_value})


def test_invalid_mutated_item_is_rejected_before_changing_target(game):
    target = character()
    equipment = item(hp_set=1)
    equipment.atk_modifier = 2
    game.player_b.table.append(target)
    game.player_a.cards_in_hand.append(equipment)
    with pytest.raises(ValueError, match="cannot combine"):
        game.play_card(game.player_a.id, equipment.id, target.id)
    assert (target.hp, target.initial_hp, target.atk) == (5, 5, 3)
    assert not target.items
    assert game.player_a.cards_in_hand == [equipment]
    assert not game.player_a.has_played_card
