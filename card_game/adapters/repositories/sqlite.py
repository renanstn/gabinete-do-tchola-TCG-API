from sqlalchemy.orm import Session

from adapters.repositories.base import BaseRepository
from adapters.repositories.models.game import Game
from adapters.repositories.models.player import Player


class SqliteRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_game_state(self, game: Game):
        existing_game = (
            self.session.query(Game).filter(Game.id == game.id).first()
        )
        if existing_game:
            existing_game.winner = game.winner
            existing_game.turn = game.turn
            existing_game.active = game.active
        else:
            self.session.add(game)
        self.session.commit()

    def list_players(self):
        return self.session.query(Player).all()

    def list_games(self):
        return self.session.query(Game).all()

    def get_game(self, game_id: int):
        return self.session.query(Game).filter(Game.id == game_id).first()
