from uuid import UUID

from application.commands import StartGamePlayer
from application.exceptions import (
    GameNotFoundError,
    InvalidGameSetupError,
    InvalidMoveError,
)
from application.ports.deck_repository import DeckRepository
from application.ports.game_repository import GameRepository
from domain.exceptions import InvalidMoveError as DomainInvalidMoveError
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
            raise GameNotFoundError(f"Game {game_id} not found.")
        return game.active_player_id

    def start_game(self, players: list[StartGamePlayer]) -> Game:
        if len(players) != 2:
            raise InvalidGameSetupError("A game requires exactly two players.")
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

    def get_game(self, game_id: UUID) -> Game:
        game = self.game_repository.get_by_id(game_id)
        if game is None:
            raise GameNotFoundError(f"Game {game_id} not found.")
        return game

    def play_card(
        self,
        game_id: UUID,
        player_id: UUID,
        card_id: str,
        target_card_id: str | None = None,
    ) -> Game:
        game = self.get_game(game_id)
        try:
            game.play_card(player_id, card_id, target_card_id)
        except DomainInvalidMoveError as error:
            raise InvalidMoveError(str(error)) from error
        self.game_repository.save(game)
        return game

    def end_turn(self, game_id: UUID, player_id: UUID) -> Game:
        game = self.get_game(game_id)
        try:
            game.end_turn(player_id)
        except DomainInvalidMoveError as error:
            raise InvalidMoveError(str(error)) from error
        self.game_repository.save(game)
        return game
