from adapters.repositories.factory import get_repository
from adapters.repositories.models.game import Game
from adapters.repositories.models.player import Player
from application.schemas.player_schema import CreatePlayerSchema


class GameService:

    repository = get_repository()

    @classmethod
    def check_turn(cls, game_id: int) -> bool:
        print(cls.repository)
        print(game_id)
        return True

    @classmethod
    def start_game(cls, players: list[CreatePlayerSchema]) -> None:
        game_players = [
            Player(
                name=player.name,
                hp=100,
                cards_in_hand="",
                table="",
                cemetery="",
            )
            for player in players
        ]
        game = Game(winner=None, turn=True, active=True, players=game_players)
        cls.repository.save_game_state(game)
