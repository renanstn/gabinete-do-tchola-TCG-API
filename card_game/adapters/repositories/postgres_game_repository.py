from pathlib import Path
from uuid import UUID

import psycopg
from adapters.repositories.game_snapshot import (
    game_from_snapshot,
    game_to_snapshot,
)
from application.ports.game_repository import GameRepository
from domain.game import Game
from psycopg.types.json import Jsonb


class PostgresGameRepository(GameRepository):
    """Persiste cada agregado Game em um snapshot JSONB transacional."""

    def __init__(self, database_url: str):
        if not database_url.strip():
            raise ValueError("A PostgreSQL database URL is required.")
        self._database_url = database_url

    def initialize_schema(self) -> None:
        """Cria o schema inicial explicitamente, fora das requisições."""
        schema = Path(__file__).with_name("postgres_schema.sql")
        with psycopg.connect(self._database_url) as connection:
            connection.execute(schema.read_text(encoding="utf-8"))

    def save(self, game: Game) -> None:
        with psycopg.connect(self._database_url) as connection:
            connection.execute(
                """
                INSERT INTO games (id, state) VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE SET state = EXCLUDED.state
                """,
                (game.id, Jsonb(game_to_snapshot(game))),
            )

    def get_by_id(self, game_id: UUID) -> Game | None:
        with psycopg.connect(self._database_url) as connection:
            row = connection.execute(
                "SELECT state FROM games WHERE id = %s", (game_id,)
            ).fetchone()
        return game_from_snapshot(row[0]) if row is not None else None
