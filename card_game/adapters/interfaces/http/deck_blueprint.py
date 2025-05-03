from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from application.game_service import GameService

deck_blueprint = Blueprint("deck", __name__, url_prefix="/deck")


@deck_blueprint.route("/hello")
def say_hi():
    return "Hi from deck blueprint!"
