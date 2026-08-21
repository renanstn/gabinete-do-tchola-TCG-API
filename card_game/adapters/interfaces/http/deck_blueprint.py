from flask import Blueprint

deck_blueprint = Blueprint("deck", __name__, url_prefix="/deck")


@deck_blueprint.route("/hello")
def say_hi() -> str:
    return "Hi from deck blueprint!"
