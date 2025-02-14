from flask import Flask

from adapters.repositories.factory import get_repository
from adapters.repositories.models.game import Game

app = Flask(__name__)


@app.route("/")
def hello_world():
    repository = get_repository()
    game = Game()
    repository.save_game_state(game)
    return "<p>Hello, World!</p>"
