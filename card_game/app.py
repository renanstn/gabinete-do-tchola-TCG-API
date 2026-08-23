from pathlib import Path

from flask import Flask

from adapters.decks.json_deck_repository import JsonDeckRepository
from adapters.interfaces.http.deck_blueprint import deck_blueprint
from adapters.interfaces.http.game_blueprint import game_blueprint
from adapters.repositories.in_memory_game_repository import (
    InMemoryGameRepository,
)
from application.game_service import GameService


def create_app(game_service: GameService | None = None) -> Flask:
    """Ponto de composição: conecta adaptadores às portas da aplicação."""
    app = Flask(__name__)
    if game_service is None:
        game_service = GameService(
            game_repository=InMemoryGameRepository(),
            deck_repository=JsonDeckRepository(
                Path(app.root_path) / "domain" / "decks"
            ),
        )

    app.extensions["game_service"] = game_service
    app.register_blueprint(game_blueprint)
    app.register_blueprint(deck_blueprint)

    @app.route("/")
    def root() -> dict[str, str]:
        return {"service": "card-game"}

    return app


app = create_app()
