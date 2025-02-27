from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from application.game_service import GameService
from application.schemas.player_schema import CreatePlayerSchema

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
    """
    Given 2 players, start a new game.
    """
    try:
        players = [
            CreatePlayerSchema(**player) for player in request.json["players"]
        ]
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    return "Game started"
