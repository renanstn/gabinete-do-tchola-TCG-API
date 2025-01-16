import uuid
from enum import Enum
from typing import List, Optional

from api.game.player import Player


class GameStatus(Enum):
    WAITING_PLAYER_A = "waiting player a"
    WAITING_PLAYER_B = "waiting player b"


class Game:
    """
    Instância de um jogo. Todo jogo tem um ID, 2 jogadores, e uma variável
    booleana que indica de qual jogador é o turno atual.
    """

    def __init__(self, player_a: Player, player_b: Player):
        self.id = uuid.uuid4()
        self.players: List[Player] = [player_a, player_b]
        self.winner = None
        self.turn = True

    @property
    def player_a(self):
        return self.players[0]

    @property
    def player_b(self):
        return self.players[1]

    def setup_game(self):
        """
        - Cada player saca 5 cartas iniciais.
        """
        for _ in range(5):
            self.player_a.draw_card()
            self.player_b.draw_card()

    def switch_turn(self):
        """
        Troca o turno do jogador A para o jogador B.
        """
        self.turn = not self.turn

    def end_play(self):
        """
        Termina a jogada de um jogador.
        - Faz as ações necessárias (cartas atacam)
        - Verifica se o outro jogador ainda está vivo
        - Passa o turno para o próximo jogador
        """
        active_player, opponent = self.player_a, self.player_b if self.turn else self.player_b, self.player_a
        self.compute_battle(active_player, opponent)
        self.switch_turn()

    def compute_battle(self, active_player: Player, opponent: Player):
        """
        Executa os passos da batalha:
        - Realiza os ataques das cartas
        - Mata as cartas cuja vida < 0
        - Ataca o herói caso não haja mais cartas para defender
        """
        for card in player.table:
            if opponent.has_cards_on_table():
                # TODO
                pass
            else:
                opponent.hp -= card.atk

    def end_game(self):
        """
        Finaliza um jogo, registra o vencedor.
        """
        pass
