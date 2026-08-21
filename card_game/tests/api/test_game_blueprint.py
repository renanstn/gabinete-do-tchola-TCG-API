from flask.testing import FlaskClient

def test_start_game(client: FlaskClient):
    player_a = {"name": "Player A", "deck_id": "a"}
    player_b = {"name": "Player B", "deck_id": "a"}

    response = client.post(
        "/game/start", json={"players": [player_a, player_b]}
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["active"] is True

    turn_response = client.get(f"/game/{body['game_id']}/active-player")
    assert turn_response.status_code == 200
    assert (
        turn_response.get_json()["active_player_id"]
        == body["active_player_id"]
    )
