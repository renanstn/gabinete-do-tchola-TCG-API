import pytest

from domain.card import Card, CardType


def test_card_initialization():
    card = Card(hp=10, atk=5, name="Test Card", card_type=CardType.CHARACTER)
    assert card.hp == 10
    assert card.atk == 5
    assert card.name == "Test Card"
    assert card.card_type == CardType.CHARACTER
    assert card.description is None
    assert card.image is None
    assert card.can_attack is False
    assert card.items == []


def test_card_id_generation():
    card = Card(hp=10, atk=5, name="Test Card", card_type=CardType.CHARACTER)
    assert card.id is not None


def test_card_take_damage():
    card = Card(hp=10, atk=5, name="Test Card", card_type=CardType.CHARACTER)
    card.take_damage(3)
    assert card.hp == 7


def test_card_is_dead():
    card = Card(hp=10, atk=5, name="Test Card", card_type=CardType.CHARACTER)
    card.take_damage(10)
    assert card.is_dead() is True


def test_card_activate():
    card = Card(hp=10, atk=5, name="Test Card", card_type=CardType.CHARACTER)
    card.activate()
    assert card.can_attack is True


def test_card_has_items():
    card = Card(hp=10, atk=5, name="Test Card", card_type=CardType.CHARACTER)
    card.items.append("item1")
    assert card.has_items() is True
