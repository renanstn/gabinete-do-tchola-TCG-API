from flask import Flask

from adapters.repositories.factory import get_repository
from adapters.repositories.models.game import Game
from adapters.repositories.models.player import Player

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
    player_01 = Player(name="Foo")
    player_02 = Player(name="Bar")
    game = Game(players=[player_01, player_02])
    repository.save_game_state(game)
    return "Done!"
