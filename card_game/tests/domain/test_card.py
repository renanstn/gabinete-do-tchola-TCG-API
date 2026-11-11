import pytest

from domain.card import Card, CardType, CharacterCard, ItemCard, StageCard


def test_card_initialization():
    card = CharacterCard(hp=10, atk=5, name="Test Card")
    assert card.hp == 10
    assert card.atk == 5
    assert card.name == "Test Card"
    assert card.card_type == CardType.CHARACTER
    assert card.description is None
    assert card.image is None
    assert card.can_attack is False
    assert card.items == []


def test_card_id_generation():
    card = CharacterCard(hp=10, atk=5, name="Test Card")
    assert card.id is not None


def test_card_take_damage():
    card = CharacterCard(hp=10, atk=5, name="Test Card")
    card.take_damage(3)
    assert card.hp == 7


def test_card_is_dead():
    card = CharacterCard(hp=10, atk=5, name="Test Card")
    card.take_damage(10)
    assert card.is_dead() is True


def test_card_activate():
    card = CharacterCard(hp=10, atk=5, name="Test Card")
    card.activate()
    assert card.can_attack is True


def test_card_has_items():
    card = CharacterCard(hp=10, atk=5, name="Test Card")
    card.apply_item(ItemCard("item1"))
    assert card.has_items() is True


@pytest.mark.parametrize("card", [ItemCard("Sword"), StageCard("Forest")])
def test_non_characters_do_not_expose_combat_state_or_actions(card):
    assert isinstance(card, Card)
    for field in (
        "hp",
        "initial_hp",
        "atk",
        "can_attack",
        "items",
        "take_damage",
        "activate",
        "apply_item",
    ):
        assert not hasattr(card, field)


def test_character_has_no_item_effect_fields():
    card = CharacterCard(5, 3, "Hero")
    for field in ("hp_modifier", "atk_modifier", "hp_set", "atk_set", "deactivate"):
        assert not hasattr(card, field)


@pytest.mark.parametrize(
    "card", [CharacterCard(5, 3, "Hero"), ItemCard("Sword"), StageCard("Forest")]
)
def test_category_cannot_be_changed(card):
    with pytest.raises(AttributeError):
        card.card_type = CardType.ITEM


@pytest.mark.parametrize("invalid", [CharacterCard(5, 3, "Hero"), StageCard("Forest")])
def test_apply_item_rejects_other_categories_without_mutation(invalid):
    target = CharacterCard(5, 3, "Target")
    with pytest.raises(TypeError, match="Only items"):
        target.apply_item(invalid)
    assert (target.hp, target.initial_hp, target.atk, target.items) == (5, 5, 3, [])


def test_base_card_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Card("Generic")
