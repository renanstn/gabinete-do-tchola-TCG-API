from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def save_game_state(self):
        pass
