from sqlalchemy import Column, Integer, String

from adapters.repositories.models.base import base


class Player(base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, required=True)
    hp = Column(Integer)
    cards_in_hand = Column(String)
    table = Column(String)
    cemetery = Column(String)
