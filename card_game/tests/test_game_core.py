from card_game.domain.game import Game
from card_game.domain.player import Player


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


def test_play_card(deck):
    """
    Cenário:
    - O player A irá abaixar uma carta
    - O player B não possui nenhuma carta baixada
    - O player A encerra seu turno
    - A carta baixada do player A não deve atacar ainda, pois cartas só podem
    atacar no próximo turno após serem baixadas
    - No próximo turno do player A, a carta deve atacar
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
    # Verifica se o player B não apanhou
    assert player_b.hp == 10
    # Verifica a mesa e a mão do player A
    assert len(player_a.table) == 1
    assert len(player_a.cards_in_hand) == 4

    # No próximo turno, a carta deve atacar
    game.end_play()
    game.end_play()
    assert player_a.table[0].can_attack is True
    assert player_b.hp == 5


def test_attack_on_hero_with_single_card(deck):
    """
    Cenário:
    - O player A possui uma carta baixada
    - O player B não possui nenhuma carta baixada
    - O player A encerra seu turno
    - A carta baixada do player A deve atacar diretamente o herói do player B
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)
    game.setup_game()

    # Player A baixa uma carta na mesa
    player_a.play_card("1")
    # Manualmente ativa a carta jogada
    player_a.table[0].activate()
    # Player A finaliza sua jogada
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # Verifica se o player B apanhou
    assert player_b.hp == 5
    # Verifica a mesa e a mão do player A
    assert len(player_a.table) == 1
    assert len(player_a.cards_in_hand) == 4


def test_attack_on_hero_with_multiple_cards(deck):
    """
    Cenário:
    - O player A possui várias cartas baixadas
    - O player B não possui nenhuma carta baixada
    - O player A encerra seu turno
    - Cada carta baixada do player A deve atacar diretamente o herói do player B
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    # Aumentamos a vida do player B para este teste
    player_b.hp = 50
    game = Game(player_a, player_b)
    game.setup_game()

    player_a.play_card("1")
    player_a.table[0].activate()
    player_a.play_card("2")
    player_a.table[1].activate()
    player_a.play_card("3")
    player_a.table[2].activate()
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # Verifica se o player B apanhou
    assert player_b.hp == 35
    # Verifica a mesa e a mão do player A
    assert len(player_a.table) == 3
    assert len(player_a.cards_in_hand) == 2


def test_attack_on_table_with_single_card(deck):
    """
    Cenário:
    - O player A possui uma carta baixada
    - O player B possui uma carta baixada
    - O player A encerra seu turno
    - A carta baixada do player A deve atacar a carta na mesa do player B
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)
    game.setup_game()

    # Player A baixa uma carta na mesa
    player_a.play_card("1")
    # Manualmente ativa a carta jogada
    player_a.table[0].activate()
    assert len(player_a.table) == 1
    # Player B baixa uma carta na mesa
    player_b.play_card("1")
    # Manualmente ativa a carta jogada
    player_b.table[0].activate()
    assert len(player_b.table) == 1
    # Player A finaliza sua jogada
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # O hero do player B não pode ter apanhado
    assert player_b.hp == 10
    # A carta na mesa do player B deve ter morrido
    assert len(player_b.table) == 0
    # A carta do player B deve ter ido parar no cemiterio
    assert len(player_b.cemetery) == 1
    # A carta do player A deve continua na mesa
    assert len(player_a.table) == 1


def test_attack_on_table_with_single_card_without_kill(deck):
    """
    Cenário:
    - O player A possui uma carta baixada
    - O player B possui uma carta baixada, com 8 de vida
    - O player A encerra seu turno
    - A carta baixada do player A deve atacar a carta na mesa do player B
    - A carta baixada do player B permanece viva, porém com menos vida
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    # Altera manualmente a vida da carta "1" para 8
    player_b.deck[0].hp = 8
    game = Game(player_a, player_b)
    game.setup_game()

    # Player A baixa uma carta na mesa
    player_a.play_card("1")
    # Manualmente ativa a carta jogada
    player_a.table[0].activate()
    assert len(player_a.table) == 1
    # Player B baixa uma carta na mesa
    player_b.play_card("1")
    # Manualmente ativa a carta jogada
    player_b.table[0].activate()
    assert len(player_b.table) == 1
    # Player A finaliza sua jogada
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # O hero do player B não pode ter apanhado
    assert player_b.hp == 10
    # A carta na mesa do player B deve estar viva
    assert len(player_b.table) == 1
    # A carta do player B deve ter sofrido dano
    assert player_b.table[0].hp == 3
    # A carta do player A deve continua na mesa
    assert len(player_a.table) == 1


def test_attack_on_table_with_multiple_cards(deck):
    """
    Cenário:
    - O player A possui duas cartas baixadas
    - O player B possui uma carta baixada, com 15 de vida
    - O player A encerra seu turno
    - As duas cartas do player A devem atacar a carta baixada do player B
    - A carta baixada do player B permanece viva, porém com menos vida
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    # Altera manualmente a vida da carta "1" para 15
    player_b.deck[0].hp = 15
    game = Game(player_a, player_b)
    game.setup_game()

    # Player A baixa duas cartas na mesa
    player_a.play_card("1")
    player_a.table[0].activate()
    player_a.play_card("2")
    player_a.table[1].activate()
    assert len(player_a.table) == 2
    # Player B baixa uma carta na mesa
    player_b.play_card("1")
    # Manualmente ativa a carta jogada
    player_b.table[0].activate()
    assert len(player_b.table) == 1
    # Player A finaliza sua jogada
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # O hero do player B não pode ter apanhado
    assert player_b.hp == 10
    # A carta na mesa do player B deve estar viva
    assert len(player_b.table) == 1
    # A carta do player B deve ter sofrido dano
    assert player_b.table[0].hp == 5
    # As cartas do player A continuam na mesa
    assert len(player_a.table) == 2


def test_attack_on_table_and_hero_with_multiple_cards(deck):
    """
    Cenário:
    - O player A possui três cartas baixadas
    - O player B possui uma carta baixada, com 8 de vida
    - O player A encerra seu turno
    - As duas cartas do player A devem atacar a carta baixada do player B
    - A carta que sobra, deve atacar o hero do player B
    - A mesa do player B fica sem cartas
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    # Altera manualmente a vida da carta "1" para 8
    player_b.deck[0].hp = 8
    game = Game(player_a, player_b)
    game.setup_game()

    # Player A baixa duas cartas na mesa
    player_a.play_card("1")
    player_a.table[0].activate()
    player_a.play_card("2")
    player_a.table[1].activate()
    player_a.play_card("3")
    player_a.table[2].activate()
    assert len(player_a.table) == 3
    # Player B baixa uma carta na mesa
    player_b.play_card("1")
    player_b.table[0].activate()
    assert len(player_b.table) == 1
    # Player A finaliza sua jogada
    game.end_play()

    # Verifica se o turno passou para o próximo jogador
    assert game.turn is False
    # O hero do player B deve ter apanhado
    assert player_b.hp == 5
    # A carta na mesa do player B deve estar morta
    assert len(player_b.table) == 0
    assert len(player_b.cemetery) == 1
    # As cartas do player A continuam na mesa
    assert len(player_a.table) == 3


def test_game_with_multiples_rounds(deck):
    """
    Testa um jogo com vários rounds.
    """
    # Preparação
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)
    game.setup_game()
    assert len(player_a.cards_in_hand) == 5
    assert len(player_b.cards_in_hand) == 5

    # Jogada do player A
    player_a.play_card("1")
    player_a.table[0].activate()
    game.end_play()
    assert len(player_a.cards_in_hand) == 4
    assert len(player_a.table) == 1
    assert player_b.hp == 5
    assert not game.turn

    # Jogada do player B
    player_b.play_card("1")
    player_b.table[0].activate()
    game.end_play()
    assert len(player_a.cards_in_hand) == 4
    assert len(player_b.table) == 1
    assert len(player_a.table) == 0
    assert len(player_a.cemetery) == 1
    assert player_a.hp == 10
    assert game.turn

    # Jogada do player A (2 cartas seguidas, apenas para testar)
    player_a.play_card("2")
    player_a.table[0].activate()
    player_a.play_card("3")
    player_a.table[1].activate()
    game.end_play()
    assert len(player_a.cards_in_hand) == 2
    assert len(player_a.table) == 2
    assert player_b.hp == 0
    assert game.winner == player_a
    assert game.active is False


def test_player_can_not_play_two_cards_on_same_turn(deck):
    """
    - Um jogador não pode baixar 2 cartas no mesmo turno.
    """
    player_a = Player("Foo", deck.copy())
    player_b = Player("Bar", deck.copy())
    game = Game(player_a, player_b)
    game.setup_game()

    player_a.play_card("1")
    player_a.play_card("2")

    assert len(player_a.table) == 1


def test_use_item_on_card():
    """
    - Deve ser possível usar itens para evoluir ou dar buff em cartas de
    personagens já baixadas na table.
    """
    pass


def test_edit_deck_add_card():
    """
    - Antes do jogo, deve ser possível editar o deck, e adicionar cartas a ele
    - Cada deck tem um limite de X cartas
    """
    pass


def test_edit_deck_remove_card():
    """
    - Antes do jogo, deve ser possível editar o deck, e remover cartas dele
    """
    pass
