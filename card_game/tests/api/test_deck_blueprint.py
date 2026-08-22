from flask.testing import FlaskClient


def test_hello(client: FlaskClient):
    response = client.get("/deck/hello")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Hi from deck blueprint!"
