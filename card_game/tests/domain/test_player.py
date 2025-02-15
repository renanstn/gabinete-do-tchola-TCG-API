import pytest

from domain.card import Card, CardType
from domain.player import Player


@pytest.fixture
def setup_deck():
    return [
        Card(hp=5, atk=3, name="Card A1", card_type=CardType.CHARACTER)
        for _ in range(10)
    ]


@pytest.fixture
def setup_player(setup_deck):
    return Player(name="Player A", deck=setup_deck)


def test_draw_card(setup_player):
    player = setup_player
    player.draw_card()
    assert len(player.cards_in_hand) == 1
    assert len(player.deck) == 9


def test_play_card(setup_player):
    player = setup_player
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    player.play_card(card_id)
    assert len(player.cards_in_hand) == 0
    assert len(player.table) == 1


def test_is_alive(setup_player):
    player = setup_player
    assert player.is_alive() == True
    player.subtract_life(10)
    assert player.is_alive() == False


def test_has_cards_on_table(setup_player):
    player = setup_player
    assert player.has_cards_on_table() == False
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    player.play_card(card_id)
    assert player.has_cards_on_table() == True


def test_get_card_by_id(setup_player):
    player = setup_player
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    card = player.get_card_by_id(card_id)
    assert card.id == card_id


def test_remove_card_from_hand(setup_player):
    player = setup_player
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    player.remove_card_from_hand(card_id)
    assert len(player.cards_in_hand) == 0


def test_remove_card_from_table(setup_player):
    player = setup_player
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    player.play_card(card_id)
    player.remove_card_from_table(card_id)
    assert len(player.table) == 0


def test_subtract_life(setup_player):
    player = setup_player
    player.subtract_life(3)
    assert player.hp == 7


def test_move_card_to_cemetery(setup_player):
    player = setup_player
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    card = player.get_card_by_id(card_id)
    player.play_card(card_id)
    player.move_card_to_cemetery(card)
    assert len(player.table) == 0
    assert len(player.cemetery) == 1


def test_can_play_card(setup_player):
    player = setup_player
    player.draw_card()
    card_id = player.cards_in_hand[0].id
    assert player.can_play_card() == True
    player.play_card(card_id)
    assert player.can_play_card() == False
