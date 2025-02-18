from flask import Flask

from adapters.repositories.factory import get_repository
from adapters.repositories.models.game import Game

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test_db")
def test_db():
    """
    Apenas um teste simples para verificar se a conexão com o banco de dados
    está funcionando.
    """
    repository = get_repository()
    game = Game()
    repository.save_game_state(game)
