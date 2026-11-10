import os
from uuid import uuid4

import psycopg
import pytest
from adapters.repositories.postgres_game_repository import (
    PostgresGameRepository,
)
from tests.adapters.test_game_snapshot import assert_same_game, populated_game


@pytest.fixture
def repository(populated_game):
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Configure TEST_DATABASE_URL para testes PostgreSQL.")
    repository = PostgresGameRepository(url)
    repository.initialize_schema()
    repository.initialize_schema()  # A inicialização deve ser idempotente.
    try:
        yield repository
    finally:
        with psycopg.connect(url) as connection:
            connection.execute(
                "DELETE FROM games WHERE id = %s", (populated_game.id,)
            )


def test_missing_game_returns_none(repository):
    assert repository.get_by_id(uuid4()) is None


def test_persists_across_repository_instances(repository, populated_game):
    repository.save(populated_game)
    another = PostgresGameRepository(os.environ["TEST_DATABASE_URL"])
    restored = another.get_by_id(populated_game.id)
    assert_same_game(restored, populated_game)
    restored.player_a.hp = 1
    assert another.get_by_id(populated_game.id).player_a.hp == 7


def test_save_updates_existing_game_and_preserves_winner(
    repository, populated_game
):
    repository.save(populated_game)
    populated_game.player_a.hp = 0
    populated_game.end_game()
    repository.save(populated_game)
    restored = repository.get_by_id(populated_game.id)
    assert_same_game(restored, populated_game)
    assert restored.winner is restored.player_b


def test_failed_write_does_not_replace_previous_state(
    repository, populated_game
):
    repository.save(populated_game)
    populated_game.player_a.name = "invalid\x00postgres-text"
    with pytest.raises(psycopg.Error):
        repository.save(populated_game)
    assert repository.get_by_id(populated_game.id).player_a.name == "João"
