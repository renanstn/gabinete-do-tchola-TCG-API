from copy import deepcopy

import pytest

from domain.card import CharacterCard, ItemCard, StageCard
from domain.exceptions import InvalidMoveError
from domain.game import Game
from domain.player import Player


def make_game():
    return Game(Player("A", []), Player("B", []))


def test_round_counts_turns_and_does_not_advance_after_victory():
    game = make_game()
    game.setup_game()
    assert game.round_number == 1
    game.end_turn(game.player_a.id)
    assert game.round_number == 2
    game.end_turn(game.player_b.id)
    assert game.round_number == 3
    game.player_b.hp = 0
    game.end_turn(game.player_a.id)
    assert game.round_number == 3


@pytest.mark.parametrize("field", ["id", "name"])
@pytest.mark.parametrize("kind", ["character", "item"])
def test_requirements_apply_to_characters_and_items(field, kind):
    game = make_game()
    ally = CharacterCard(5, 2, "Ally")
    stage = StageCard("Forest")
    game.player_a.table.append(ally)
    game.active_stage = stage
    requirements = {
        "active_stage": {field: getattr(stage, field)},
        "card_on_table": {field: getattr(ally, field)},
    }
    card = (
        CharacterCard(3, 1, "New", play_requirements=requirements)
        if kind == "character"
        else ItemCard("Sword", atk_modifier=2, play_requirements=requirements)
    )
    game.player_a.cards_in_hand.append(card)
    game.play_card(game.player_a.id, card.id, ally.id if kind == "item" else None)
    assert card not in game.player_a.cards_in_hand
    assert game.player_a.has_played_card


@pytest.mark.parametrize(
    "failure", ["no_stage", "wrong_stage", "opponent", "hand", "cemetery"]
)
def test_unsatisfied_requirements_do_not_mutate_game(failure):
    from adapters.repositories.game_snapshot import game_to_snapshot

    game = make_game()
    ally = CharacterCard(5, 2, "Ally")
    game.active_stage = StageCard("Forest")
    game.player_a.table.append(ally)
    card = CharacterCard(
        3,
        1,
        "New",
        play_requirements={
            "active_stage": {"name": "Forest"},
            "card_on_table": {"name": "Ally"},
        },
    )
    game.player_a.cards_in_hand.append(card)
    if failure == "no_stage":
        game.active_stage = None
    elif failure == "wrong_stage":
        game.active_stage = StageCard("Desert")
    else:
        game.player_a.table.remove(ally)
        if failure == "opponent":
            game.player_b.table.append(ally)
        else:
            getattr(
                game.player_a, "cards_in_hand" if failure == "hand" else "cemetery"
            ).append(ally)
    before = deepcopy(game_to_snapshot(game))
    with pytest.raises(InvalidMoveError):
        game.play_card(game.player_a.id, card.id)
    assert game_to_snapshot(game) == before


@pytest.mark.parametrize(
    "requirements",
    [
        [],
        {"unknown": {"name": "X"}},
        {"active_stage": "Forest"},
        {"card_on_table": {}},
        {"card_on_table": {"name": ""}},
        {"active_stage": {"id": "x", "name": "X"}},
    ],
)
def test_invalid_requirements_are_rejected(requirements):
    with pytest.raises(ValueError):
        StageCard("Stage", play_requirements=requirements)
