from unittest.mock import patch

from adapters.repositories.in_memory_game_repository import (
    InMemoryGameRepository,
)
from adapters.repositories.postgres_game_repository import (
    PostgresGameRepository,
)
from app import create_app
from application.game_service import GameService


def test_default_repository_is_in_memory(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    app = create_app()
    assert isinstance(
        app.extensions["game_service"].game_repository, InMemoryGameRepository
    )
    result = app.test_cli_runner().invoke(args=["init-db"])
    assert result.exit_code != 0
    assert "DATABASE_URL" in result.output


def test_database_url_selects_postgres_and_explicit_schema_initialization(
    monkeypatch,
):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/card_game")
    with patch.object(
        PostgresGameRepository, "initialize_schema"
    ) as initialize:
        app = create_app()
        assert isinstance(
            app.extensions["game_service"].game_repository,
            PostgresGameRepository,
        )
        initialize.assert_not_called()
        result = app.test_cli_runner().invoke(args=["init-db"])
        assert result.exit_code == 0
        initialize.assert_called_once_with()


def test_injected_service_overrides_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/card_game")
    service = GameService(InMemoryGameRepository(), deck_repository=None)
    assert create_app(service).extensions["game_service"] is service
