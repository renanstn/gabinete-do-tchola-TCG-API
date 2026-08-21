from flask.testing import FlaskClient


def test_hello_world(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"service": "card-game"}
