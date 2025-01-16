from api.game.card import Card, CardType
from api.game.game import Game
from api.game.player import Player


def test_new_game(deck):
    """
    Dado 2 players, ambos com um deck de 5 cartas, deve ser possível iniciar um
    game. Cada player sacará 5 cartas, esgotando seus respectivos decks.
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)

    game.setup_game()

    assert game.turn == True
    # Verifica se cad aplayer tem 5 cartas na mão
    assert len(player_a.cards_in_hand) == 5
    assert len(player_b.cards_in_hand) == 5
    # Verifica se os decks de ambos esgotou
    assert len(player_a.deck) == 0
    assert len(player_b.deck) == 0


def test_basic_attack_on_hero(deck):
    """
    Cenário:
    - O player A possui cartas baixadas
    - O player B não possui nenhuma carta baixada
    - O player A encerra seu turno
    - Cada carta baixada do player A deve atacar diretamente o herói do player B
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)
    game.setup_game()

    # Player A baixa uma carta na mesa
    player_a.play_card("1")
    # Player A finaliza sua jogada
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # Verifica se o player B apanhou
    assert player_b.hp == 5
    # Verifica a mesa e a mão do player A
    assert len(player_a.table) == 1
    assert len(player_a.cards_in_hand) == 4
