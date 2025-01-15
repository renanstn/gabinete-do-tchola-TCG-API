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

    def __init__(
        self, player_a: Player, player_b: Player, winner: Player = None
    ):
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
        pass


def setup_game():
    """
    Executa o setup inicial do jogo:
    - Embaralha as cartas de ambos os jogadores
    - Saca as cartas iniciais de cada jogador
    - Registra quem deve ser o jogador inicial
    """
    pass


def run_battle():
    """
    Executa os passos da batalha:
    - Realiza os ataques das cartas
    - Mata as cartas cuja vida < 0
    - Ataca o herói caso não haja mais cartas para defender
    """
    pass


def end_game():
    """
    Registra o fim de um jogo, finaliza no banco de dados, registra o vencedor.
    """
    pass


def draw_card(player_id: str):
    """
    Permite que o jogador saque uma carta aleatória do seu deck.
    """
    pass


def play_card(player_id: str, card: str):
    """
    Registra uma carta baixada na mesa por um jogador.
    """
    pass
