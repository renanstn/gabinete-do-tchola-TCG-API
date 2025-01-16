import random
import uuid
from typing import List

from api.game.player import Player


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
        - Embaralha os decks dos players
        - Cada player saca 5 cartas iniciais.
        """
        random.shuffle(self.player_a.deck)
        random.shuffle(self.player_b.deck)
        for _ in range(5):
            self.player_a.draw_card()
            self.player_b.draw_card()
        print("Game ready")

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
        if self.turn:
            active_player, opponent = self.player_a, self.player_b
        else:
            active_player, opponent = self.player_b, self.player_a
        print(f"Player {active_player.name} ends its turn")
        self.compute_battle(active_player, opponent)
        self.switch_turn()

    def compute_battle(self, active_player: Player, opponent: Player):
        """
        Executa os passos da batalha:
        - Realiza os ataques das cartas
        - Mata as cartas cuja vida < 0
        - Ataca o herói caso não haja mais cartas para defender
        """
        for card in active_player.table:
            if opponent.has_cards_on_table():
                for enemy_card in opponent.table:
                    enemy_card.take_damage(card.atk)
                    if enemy_card.is_dead():
                        opponent.move_card_to_cemetery(enemy_card)
            else:
                print(opponent.hp)
                opponent.subtract_life(card.atk)

    def end_game(self):
        """
        Finaliza um jogo, registra o vencedor.
        """
        pass
