from flask.testing import FlaskClient


def test_start_game(client: FlaskClient):
    player_a = {"name": "Player A", "deck_id": "1"}
    player_b = {"name": "Player B", "deck_id": "2"}

    response = client.post(
        "/game/start", json={"players": [player_a, player_b]}
    )

    assert response.status_code == 200
