from sqlalchemy import Boolean, Column, Integer, String

from adapters.repositories.models.base import base


class Game(base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    # players = Column()  # FIXME
    winner = Column(String)
    turn = Column(Boolean)
    active = Column(Boolean)
