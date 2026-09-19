from uuid import UUID

from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError

from adapters.interfaces.http.schemas import CreatePlayerRequest
from application.commands import StartGamePlayer
from application.exceptions import ApplicationError, GameNotFoundError

game_blueprint = Blueprint("game", __name__, url_prefix="/game")


@game_blueprint.route("/hello")
def say_hi() -> str:
    return "Hi from game blueprint!"


@game_blueprint.route("/<uuid:game_id>/active-player")
def get_active_player(game_id: UUID):
    service = current_app.extensions["game_service"]
    try:
        active_player_id = service.get_active_player_id(game_id)
    except ApplicationError as error:
        return jsonify({"error": str(error)}), 404
    return jsonify({"game_id": str(game_id), "active_player_id": str(active_player_id)})


@game_blueprint.route("/start", methods=["POST"])
def start_game():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"errors": [{"msg": "JSON body invalid."}]}), 400

    try:
        players = [CreatePlayerRequest(**player) for player in payload["players"]]
    except (KeyError, TypeError, ValidationError) as error:
        errors = (
            error.errors()
            if isinstance(error, ValidationError)
            else [{"msg": str(error)}]
        )
        return jsonify({"errors": errors}), 400

    command = [
        StartGamePlayer(name=player.name, deck_id=player.deck_id) for player in players
    ]
    try:
        game = current_app.extensions["game_service"].start_game(command)
    except ApplicationError as error:
        return jsonify({"error": str(error)}), 400

    return (
        jsonify(
            {
                "game_id": str(game.id),
                "active": game.active,
                "active_player_id": str(game.active_player_id),
            }
        ),
        201,
    )


def serialize_game(game):
    """Estado completo para o testador local (inclui as duas mãos)."""

    def serialize_card(card):
        return {
            "id": card.id,
            "name": card.name,
            "hp": card.hp,
            "atk": card.atk,
            "card_type": card.card_type.value,
            "description": card.description,
            "can_attack": card.can_attack,
            "hp_modifier": card.hp_modifier,
            "atk_modifier": card.atk_modifier,
            "deactivate": card.deactivate,
            "items": [serialize_card(item) for item in card.items],
        }

    return {
        "game_id": str(game.id),
        "active": game.active,
        "active_player_id": str(game.active_player_id),
        "winner_id": str(game.winner.id) if game.winner else None,
        "players": [
            {
                "id": str(player.id),
                "name": player.name,
                "hp": player.hp,
                "deck_count": len(player.deck),
                "can_play_card": player.can_play_card(),
                "can_play_item": not player.has_played_card,
                **{
                    zone: [serialize_card(card) for card in getattr(player, zone)]
                    for zone in ("cards_in_hand", "table", "cemetery")
                },
            }
            for player in game.players
        ],
    }


@game_blueprint.get("/<uuid:game_id>")
def get_game(game_id: UUID):
    try:
        game = current_app.extensions["game_service"].get_game(game_id)
        return jsonify(serialize_game(game))
    except GameNotFoundError as error:
        return jsonify({"error": str(error)}), 404


@game_blueprint.post("/<uuid:game_id>/play-card")
@game_blueprint.post("/<uuid:game_id>/end-turn")
def make_move(game_id: UUID):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON body invalid."}), 400
    try:
        player_id = UUID(str(payload.get("player_id", "")))
    except ValueError:
        return jsonify({"error": "player_id must be a valid UUID."}), 400
    service = current_app.extensions["game_service"]
    try:
        if request.path.endswith("/play-card"):
            card_id = payload.get("card_id")
            if not isinstance(card_id, str) or not card_id:
                return jsonify({"error": "card_id is required."}), 400
            target_card_id = payload.get("target_card_id")
            if target_card_id is not None and (
                not isinstance(target_card_id, str) or not target_card_id
            ):
                return (
                    jsonify({"error": "target_card_id must be a non-empty string."}),
                    400,
                )
            game = service.play_card(game_id, player_id, card_id, target_card_id)
        else:
            game = service.end_turn(game_id, player_id)
        return jsonify(serialize_game(game))
    except GameNotFoundError as error:
        return jsonify({"error": str(error)}), 404
    except ApplicationError as error:
        return jsonify({"error": str(error)}), 400
