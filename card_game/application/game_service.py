from adapters.repositories.factory import get_repository


class GameService:

    repository = get_repository()

    @classmethod
    def check_turn(cls, game_id: int) -> bool:
        print(cls.repository)
        print(game_id)
        return True

    @classmethod
    def start_game(cls, players):
        # TODO Store player A
        # TODO Store player B
        # TODO Create a new game
        # TODO Store the game
        pass
