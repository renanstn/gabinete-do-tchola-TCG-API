from flask.testing import FlaskClient

from adapters.repositories.factory import get_repository


def test_start_game(client: FlaskClient):
    player_a = {"name": "Player A", "deck_id": "1"}
    player_b = {"name": "Player B", "deck_id": "2"}

    response = client.post(
        "/game/start", json={"players": [player_a, player_b]}
    )

    assert response.status_code == 200
    repository = get_repository()
    # Assert two players was created
    assert len(repository.list_players()) == 2
    # Assert game was created
    assert len(repository.list_games()) == 1
    # Assert player names are correct
    assert repository.list_players()[0].name == player_a["name"]
    assert repository.list_players()[1].name == player_b["name"]
    # Assert game state is correct
    game = repository.list_games()[0]
    assert game.winner is None
    assert game.turn is True
    assert game.active is True
