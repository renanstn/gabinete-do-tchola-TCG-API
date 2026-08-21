from abc import ABC, abstractmethod
from uuid import UUID

from domain.game import Game


class GameRepository(ABC):
    """Porta de saída para armazenamento de partidas."""

    @abstractmethod
    def save(self, game: Game) -> None:
        pass

    @abstractmethod
    def get_by_id(self, game_id: UUID) -> Game | None:
        pass
