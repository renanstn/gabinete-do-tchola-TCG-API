import random
import uuid

from domain.player import Player


class Game:
    """
    Instância de um jogo. Todo jogo tem um ID, dois jogadores e identifica
    explicitamente o jogador que possui o turno atual.
    """

    def __init__(self, player_a: Player, player_b: Player):
        self.id: uuid.UUID = uuid.uuid4()
        self.players: list[Player] = [player_a, player_b]
        self.winner: Player | None = None
        self.active_player_id: uuid.UUID = player_a.id
        self.active: bool = True

    @property
    def player_a(self) -> Player:
        return self.players[0]

    @property
    def player_b(self) -> Player:
        return self.players[1]

    def setup_game(self) -> None:
        """
        - Embaralha os decks dos players
        - Cada player saca 5 cartas iniciais.
        """
        random.shuffle(self.player_a.deck)
        random.shuffle(self.player_b.deck)
        for _ in range(5):
            self.player_a.draw_card()
            self.player_b.draw_card()

    def switch_turn(self) -> None:
        """
        Passa o turno para o oponente do jogador ativo.
        """
        _, opponent = self.get_active_player_and_opponent()
        self.active_player_id = opponent.id

    def get_active_player_and_opponent(self) -> tuple[Player, Player]:
        if self.active_player_id == self.player_a.id:
            return self.player_a, self.player_b
        if self.active_player_id == self.player_b.id:
            return self.player_b, self.player_a
        raise RuntimeError("O jogador ativo não pertence a esta partida.")

    def end_play(self) -> None:
        """
        Termina a jogada de um jogador.
        - Faz as ações necessárias (cartas atacam)
        - Verifica se o outro jogador ainda está vivo
        - Ativa as cartas recém baixadas
        - Passa o turno para o próximo jogador
        """
        active_player, opponent = self.get_active_player_and_opponent()
        self.compute_battle(active_player, opponent)
        for card in active_player.table:
            card.activate()
        if opponent.is_alive():
            self.switch_turn()
        else:
            self.end_game()

    def compute_battle(self, active_player: Player, opponent: Player) -> None:
        """
        Executa os passos da batalha:
        - Realiza os ataques das cartas baixadas na mesa
        - Mata as cartas cuja vida < 0
        - Ataca o herói caso não haja mais cartas para defender
        """
        for card in active_player.table:
            if not card.can_attack:
                continue
            if opponent.has_cards_on_table():
                for enemy_card in opponent.table:
                    enemy_card.take_damage(card.atk)
                    if enemy_card.is_dead():
                        opponent.move_card_to_cemetery(enemy_card)
            else:
                opponent.subtract_life(card.atk)

    def end_game(self) -> None:
        """
        Finaliza um jogo, registra o vencedor.
        """
        self.winner = self.player_a if self.player_a.hp > 0 else self.player_b
        self.active = False
