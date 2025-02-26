"""
This script aims to be run once to create the tables in the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.repositories.models.base import base
# Necessary imports to create the tables
from adapters.repositories.models.game import Game
from adapters.repositories.models.player import Player
from config import PostgresConfig, SQLiteConfig

engine = create_engine(SQLiteConfig.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def create_tables():
    print(f"Creating tables: {base.metadata.tables.keys()}")
    base.metadata.create_all(engine)
    print("Tables created!")


if __name__ == "__main__":
    create_tables()
