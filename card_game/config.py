import os


class DatabaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class SQLiteConfig(DatabaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"


class PostgresConfig(DatabaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/app"
    )


class AppSettings:
    REPOSITORY = os.getenv("REPOSITORY", "sqlite")
