from adapters.repositories.factory import get_repository

class GameService:

    repository = get_repository()

    @classmethod
    def check_turn(cls, game_id: int) -> bool:
        print(cls.repository)
        return True
