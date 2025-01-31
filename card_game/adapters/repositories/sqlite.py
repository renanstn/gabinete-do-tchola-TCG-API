from sqlalchemy.orm import Session

from card_game.adapters.repositories.base import BaseRepository
from card_game.adapters.repositories.models.game import Game


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
