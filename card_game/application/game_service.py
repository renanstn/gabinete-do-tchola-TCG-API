from uuid import UUID

from application.commands import StartGamePlayer
from application.exceptions import GameNotFoundError, InvalidGameSetupError
from application.ports.deck_repository import DeckRepository
from application.ports.game_repository import GameRepository
from domain.game import Game
from domain.player import Player


class GameService:
    """Casos de uso de partida; não conhece Flask, SQLAlchemy ou arquivos."""

    def __init__(
        self,
        game_repository: GameRepository,
        deck_repository: DeckRepository,
    ):
        self.game_repository = game_repository
        self.deck_repository = deck_repository

    def get_active_player_id(self, game_id: UUID) -> UUID:
        game = self.game_repository.get_by_id(game_id)
        if game is None:
            raise GameNotFoundError(f"Partida {game_id} não encontrada.")
        return game.active_player_id

    def start_game(self, players: list[StartGamePlayer]) -> Game:
        if len(players) != 2:
            raise InvalidGameSetupError(
                "Uma partida exige exatamente dois jogadores."
            )
        game_players = [
            Player(
                name=player.name,
                deck=self.deck_repository.get_cards(player.deck_id),
            )
            for player in players
        ]
        game = Game(game_players[0], game_players[1])
        game.setup_game()
        self.game_repository.save(game)
        return game

    def play_card(self, game_id: UUID, player_id: UUID, card_id: UUID) -> None:
        game = self.game_repository.get_by_id(game_id)
        if game is None:
            raise GameNotFoundError(f"Partida {game_id} não encontrada.")
        if game.active_player_id != player_id:
            raise InvalidTurnError("Não é a vez deste jogador.")
        card = game.get_card(card_id)
        if card is None:
            raise CardNotFoundError(f"Cartão {card_id} não encontrado.")
        game.play_card(card)
        self.game_repository.save(game)

    def end_turn(self, game_id: UUID, player_id: UUID) -> None:
        game = self.game_repository.get_by_id(game_id)
        if game is None:
            raise GameNotFoundError(f"Partida {game_id} não encontrada.")
        if game.active_player_id != player_id:
            raise InvalidTurnError("Não é a vez deste jogador.")
        game.end_turn()
        self.game_repository.save(game)
