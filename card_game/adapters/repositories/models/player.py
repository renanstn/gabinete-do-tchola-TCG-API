from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from adapters.repositories.models.base import base
from adapters.repositories.models.game import game_players


class Player(base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hp = Column(Integer)
    cards_in_hand = Column(String)
    table = Column(String)
    cemetery = Column(String)

    games = relationship(
        "Game", secondary=game_players, back_populates="players"
    )
