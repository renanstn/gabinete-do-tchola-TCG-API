import json
from uuid import UUID, uuid4

import pytest

from adapters.decks.json_deck_repository import JsonDeckRepository
from application.exceptions import DeckNotFoundError


DECK_ID = UUID("6c2e32a4-644d-4be5-bd8a-62b683b08757")


def write_deck(path, deck_id):
    path.write_text(
        json.dumps(
            {
                "id": deck_id,
                "cards": [
                    {"name": "Zora", "card_type": "character", "hp": 4, "atk": 2}
                ],
            }
        ),
        encoding="utf-8",
    )


def test_finds_deck_by_internal_id_after_renaming_file(tmp_path):
    write_deck(tmp_path / "a_different_deck.json", str(uuid4()))
    path = tmp_path / "deck_a.json"
    write_deck(path, str(DECK_ID).upper())
    repository = JsonDeckRepository(tmp_path)
    first = repository.get_cards(DECK_ID)
    path.rename(tmp_path / "personagens.json")
    second = repository.get_cards(DECK_ID)
    assert first[0].name == second[0].name == "Zora"
    assert first[0].id != second[0].id
    first[0].take_damage(1)
    assert second[0].hp == 4


def test_filename_does_not_match_a_different_internal_id(tmp_path):
    write_deck(tmp_path / f"deck_{DECK_ID}.json", str(uuid4()))
    with pytest.raises(DeckNotFoundError):
        JsonDeckRepository(tmp_path).get_cards(DECK_ID)


def test_skips_definitions_without_valid_id(tmp_path):
    (tmp_path / "a_missing_id.json").write_text('{"cards": []}')
    write_deck(tmp_path / "b_invalid_id.json", "invalid")
    write_deck(tmp_path / "deck_a.json", str(DECK_ID))
    assert len(JsonDeckRepository(tmp_path).get_cards(DECK_ID)) == 1


def test_bundled_decks_are_loadable_from_resources():
    from pathlib import Path

    decks_path = Path(__file__).resolve().parents[2] / "resources" / "decks"
    definitions = list(decks_path.glob("*.json"))
    assert definitions
    repository = JsonDeckRepository(decks_path)
    for path in definitions:
        definition = json.loads(path.read_text(encoding="utf-8"))
        cards = repository.get_cards(UUID(definition["id"]))
        assert len(cards) == len(definition["cards"])
        assert [card.name for card in cards] == [
            card["name"] for card in definition["cards"]
        ]


@pytest.mark.parametrize("absolute", [False, True])
def test_loads_item_effects_and_creates_independent_instances(tmp_path, absolute):
    from domain.card import CardType

    (tmp_path / "items.json").write_text(
        json.dumps(
            {
                "id": str(DECK_ID),
                "cards": [
                    {
                        "name": "Curse",
                        "card_type": "item",
                        "hp_modifier": 0 if absolute else -2,
                        "atk_modifier": 0 if absolute else -1,
                        "deactivate": True,
                        "hp_set": 1 if absolute else None,
                        "atk_set": 0 if absolute else None,
                    }
                ],
            }
        )
    )
    repository = JsonDeckRepository(tmp_path)
    first = repository.get_cards(DECK_ID)[0]
    second = repository.get_cards(DECK_ID)[0]
    assert first.card_type == CardType.ITEM
    assert (first.hp_set, first.atk_set) == ((1, 0) if absolute else (None, None))
    assert (first.hp_modifier, first.atk_modifier, first.deactivate) == (
        (0, 0, True) if absolute else (-2, -1, True)
    )
    assert first.id != second.id
    first.atk_modifier = 99
    assert second.atk_modifier == (0 if absolute else -1)


def test_deck_loader_rejects_mixed_item_effect_modes():
    with pytest.raises(ValueError, match="cannot combine"):
        JsonDeckRepository._to_card(
            {
                "name": "Invalid",
                "card_type": "item",
                "hp_set": 1,
                "atk_modifier": 2,
            }
        )


def test_loads_each_concrete_card_type():
    from domain.card import CharacterCard, ItemCard, StageCard

    for definition, expected in [
        ({"name": "Hero", "card_type": "character", "hp": 5, "atk": 2}, CharacterCard),
        ({"name": "Sword", "card_type": "item", "atk_modifier": 2}, ItemCard),
        ({"name": "Forest", "card_type": "stage"}, StageCard),
    ]:
        assert isinstance(JsonDeckRepository._to_card(definition), expected)
