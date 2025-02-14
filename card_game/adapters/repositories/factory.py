from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.repositories.sqlite import SqliteRepository
# from adapters.repositories.postgres import PostgresRepository
from config import AppSettings, PostgresConfig, SQLiteConfig


def get_repository():
    if AppSettings.REPOSITORY == "sqlite":
        engine = create_engine(SQLiteConfig.SQLALCHEMY_DATABASE_URI)
        LocalSession = sessionmaker(bind=engine)
        db_session = LocalSession()
        return SqliteRepository(db_session)
    elif AppSettings.REPOSITORY == "postgres":
        # return PostgresRepository()
        pass
    else:
        raise ValueError("Repository not found")
