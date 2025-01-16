from api.game.card import Card, CardType
from api.game.game import Game
from api.game.player import Player


def test_new_game(player_with_default_deck):
    """
    Dado 2 players e um deck default para cada, deve ser possível iniciar um game.
    """
    player_a = player_with_default_deck
    player_b = player_with_default_deck
    game = Game(player_a, player_b)

    game.setup_game()

    assert game.turn == True
    assert len(player_a.cards_in_hand) == 5
    assert len(player_b.cards_in_hand) == 5

def test_basic_attack_on_hero(player_with_default_deck):
    """
    Cenário:
    - O player A possui cartas baixadas
    - O player B não possui nenhuma carta baixada
    - O player A encerra seu turno
    - Cada carta baixada do player A deve atacar diretamente o herói do player B
    """
    player_a = player_with_default_deck
    player_b = player_with_default_deck
    game = Game(player_a, player_b)
    game.setup_game()

    player_a.play_card("1")
    game.end_play()

    assert game.turn is False
    assert player_b.hp == 5
    assert len(player_a.table) == 1
    assert len(player_a.cards_in_hand) == 4
