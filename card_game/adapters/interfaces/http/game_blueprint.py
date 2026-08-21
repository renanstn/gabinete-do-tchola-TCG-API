from uuid import UUID

from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

from adapters.interfaces.http.schemas import CreatePlayerRequest
from application.commands import StartGamePlayer
from application.exceptions import ApplicationError

game_blueprint = Blueprint("game", __name__, url_prefix="/game")


@game_blueprint.route("/<uuid:game_id>/check-turn")
def check_turn(game_id: UUID):
    service = current_app.extensions["game_service"]
    try:
        is_first_player_turn = service.check_turn(game_id)
    except ApplicationError as error:
        return jsonify({"error": str(error)}), 404
    return jsonify(
        {"game_id": str(game_id), "is_first_player_turn": is_first_player_turn}
    )


@game_blueprint.route("/start", methods=["POST"])
def start_game():
    """
    Given 2 players, start a new game.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"errors": [{"msg": "Corpo JSON inválido."}]}), 400

    try:
        players = [
            CreatePlayerRequest(**player) for player in payload["players"]
        ]
    except (KeyError, TypeError, ValidationError) as error:
        errors = (
            error.errors()
            if isinstance(error, ValidationError)
            else [{"msg": str(error)}]
        )
        return jsonify({"errors": errors}), 400

    command = [
        StartGamePlayer(name=player.name, deck_id=player.deck_id)
        for player in players
    ]
    try:
        game = current_app.extensions["game_service"].start_game(command)
    except ApplicationError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"game_id": str(game.id), "active": game.active}), 201
