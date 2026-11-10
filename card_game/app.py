import os
from pathlib import Path

import click
from adapters.decks.json_deck_repository import JsonDeckRepository
from adapters.interfaces.http.deck_blueprint import deck_blueprint
from adapters.interfaces.http.game_blueprint import game_blueprint
from adapters.repositories.in_memory_game_repository import (
    InMemoryGameRepository,
)
from adapters.repositories.postgres_game_repository import (
    PostgresGameRepository,
)
from application.game_service import GameService
from flask import Flask
from flask_cors import CORS


def create_app(game_service: GameService | None = None) -> Flask:
    """Ponto de composição: conecta adaptadores às portas da aplicação."""
    app = Flask(__name__)
    CORS(app)
    if game_service is None:
        database_url = os.environ.get("DATABASE_URL")
        game_service = GameService(
            game_repository=(
                PostgresGameRepository(database_url)
                if database_url is not None
                else InMemoryGameRepository()
            ),
            deck_repository=JsonDeckRepository(
                Path(app.root_path) / "resources" / "decks"
            ),
        )

    app.extensions["game_service"] = game_service

    @app.cli.command("init-db")
    def init_db() -> None:
        """Cria as tabelas no PostgreSQL configurado para esta aplicação."""
        repository = app.extensions["game_service"].game_repository
        if not isinstance(repository, PostgresGameRepository):
            raise click.ClickException(
                "Configure DATABASE_URL para usar PostgreSQL."
            )
        repository.initialize_schema()
        click.echo("Schema PostgreSQL inicializado.")

    app.register_blueprint(game_blueprint)
    app.register_blueprint(deck_blueprint)

    @app.route("/")
    def root() -> dict[str, str]:
        return {"service": "card-game"}

    return app


app = create_app()
