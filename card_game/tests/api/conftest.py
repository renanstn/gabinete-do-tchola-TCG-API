import pytest

from app import app


@pytest.fixture
def client():
    test_app = app
    test_app.config["TESTING"] = True
    with test_app.test_client() as client:
        yield client
