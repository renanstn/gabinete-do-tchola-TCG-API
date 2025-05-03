from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def save_game_state(self):
        pass

    @abstractmethod
    def list_players(self):
        pass

    @abstractmethod
    def list_games(self):
        pass
