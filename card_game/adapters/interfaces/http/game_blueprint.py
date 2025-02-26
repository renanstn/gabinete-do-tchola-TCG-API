from flask import Blueprint, request

game_blueprint = Blueprint("game", __name__, url_prefix="/game")


@game_blueprint.route("/hello")
def say_hi():
    return "Hi from games!"


@game_blueprint.route("/start", methods=["POST"])
def start_game():
    data = request.json
    print(data)
    return "Game started"
