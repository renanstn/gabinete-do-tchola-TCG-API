from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from adapters.repositories.models.base import base

game_players = Table(
    "game_players",
    base.metadata,
    Column("game_id", Integer, ForeignKey("games.id"), primary_key=True),
    Column("player_id", Integer, ForeignKey("players.id"), primary_key=True),
)


class Game(base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    winner = Column(String)
    turn = Column(Boolean, default=True)
    active = Column(Boolean, default=True)

    players = relationship(
        "Player", secondary=game_players, back_populates="games"
    )
