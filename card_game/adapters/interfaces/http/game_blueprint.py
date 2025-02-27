from flask import Blueprint, request
from application.game_service import GameService

game_blueprint = Blueprint("game", __name__, url_prefix="/game")


@game_blueprint.route("/hello")
def say_hi():
    return "Hi from games!"


@game_blueprint.route("/<game_id>/check_turn")
def check_turn(game_id: int):
    """
    curl -X GET "http://localhost:5000/game/1/check_turn"
    """
    print(game_id)
    GameService.check_turn(game_id)
    return "todo"


@game_blueprint.route("/start", methods=["POST"])
def start_game():
    data = request.json
    print(data)
    return "Game started"
