import logging
import random
import uuid

from domain.card import CardType
from domain.exceptions import InvalidMoveError
from domain.player import Player


logger = logging.getLogger(__name__)


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
        - O jogador ativo compra uma carta ao iniciar o primeiro turno.
        """
        logger.debug("Shuffling decks and drawing initial cards")
        random.shuffle(self.player_a.deck)
        random.shuffle(self.player_b.deck)
        for _ in range(5):
            self.player_a.draw_card()
            self.player_b.draw_card()
        self.start_turn()

    def start_turn(self) -> None:
        """Compra uma carta para o jogador que está iniciando o turno."""
        active_player, _ = self.get_active_player_and_opponent()
        active_player.has_played_card = False
        active_player.draw_card()

    def switch_turn(self) -> None:
        """
        Passa o turno para o oponente e realiza sua compra de início de turno.
        """
        _, opponent = self.get_active_player_and_opponent()
        self.active_player_id = opponent.id
        self.start_turn()
        logger.debug("Switching turn to opponent")

    def get_active_player_and_opponent(self) -> tuple[Player, Player]:
        if self.active_player_id == self.player_a.id:
            return self.player_a, self.player_b
        if self.active_player_id == self.player_b.id:
            return self.player_b, self.player_a
        raise RuntimeError("The active player does not belong to this game.")

    def _validate_turn(self, player_id: uuid.UUID) -> None:
        if not self.active:
            raise InvalidMoveError("The game has already ended.")
        if self.active_player_id != player_id:
            raise InvalidMoveError("It is not this player's turn.")

    def play_card(
        self, player_id: uuid.UUID, card_id: str, target_card_id: str | None = None
    ) -> None:
        self._validate_turn(player_id)
        active_player, _ = self.get_active_player_and_opponent()
        card = active_player.get_card_by_id(card_id)
        if card.card_type != CardType.ITEM:
            if target_card_id is not None:
                raise InvalidMoveError("Only items accept a target.")
            active_player.play_card(card_id)
            return
        if active_player.has_played_card:
            raise InvalidMoveError("You have already played a card this turn.")
        for owner in self.players:
            for target in owner.table:
                if (
                    target.id == target_card_id
                    and target.card_type == CardType.CHARACTER
                ):
                    target.apply_item(card)
                    active_player.remove_card_from_hand(card.id)
                    active_player.has_played_card = True
                    if target.is_dead():
                        owner.move_card_to_cemetery(target)
                    return
        raise InvalidMoveError(
            "Items require a character target on either player's table."
        )

    def end_turn(self, player_id: uuid.UUID) -> None:
        """
        Termina a jogada de um jogador.
        - Faz as ações necessárias (cartas atacam)
        - Verifica se o outro jogador ainda está vivo
        - Ativa as cartas recém baixadas
        - Passa o turno para o próximo jogador
        """
        self._validate_turn(player_id)
        logger.debug("Ending turn")
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
        logger.debug("Computing battle...")
        for card in active_player.table:
            if not card.can_attack:
                logger.debug(f"Card {card.name} cannot attack yet")
                continue
            if opponent.has_cards_on_table():
                target = opponent.get_next_card_target()
                logger.debug(f"Card {card.name} attacking {target.name}")
                target.take_damage(card.atk)
                if target.is_dead():
                    logger.debug(f"Card {card.atk} killed {target.name}")
                    opponent.move_card_to_cemetery(target)
            else:
                logger.debug(f"Card {card.atk} attacked the hero")
                opponent.subtract_life(card.atk)

    def end_game(self) -> None:
        """
        Finaliza um jogo, registra o vencedor.
        """
        logger.debug("Ending game...")
        self.winner = self.player_a if self.player_a.hp > 0 else self.player_b
        self.active = False
