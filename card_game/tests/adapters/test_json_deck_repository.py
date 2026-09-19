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
