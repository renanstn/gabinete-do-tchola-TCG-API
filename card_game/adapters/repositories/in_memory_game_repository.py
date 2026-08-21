from uuid import UUID

from application.ports.game_repository import GameRepository
from domain.game import Game


class InMemoryGameRepository(GameRepository):
    """Adaptador simples para desenvolvimento e testes."""

    def __init__(self):
        self.games: dict[UUID, Game] = {}

    def save(self, game: Game) -> None:
        self.games[game.id] = game

    def get_by_id(self, game_id: UUID) -> Game | None:
        return self.games.get(game_id)
