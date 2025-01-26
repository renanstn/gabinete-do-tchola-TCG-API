from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    # players = Column()  # FIXME
    winner = Column(String)
    turn = Column(Boolean)
    active = Column(Boolean)
