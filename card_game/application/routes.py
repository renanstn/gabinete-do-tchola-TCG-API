from flask import Blueprint

game_blueprint = Blueprint("game", __name__)


@game_blueprint.route("/game/start", methods=["POST"])
def start_game():
    pass
