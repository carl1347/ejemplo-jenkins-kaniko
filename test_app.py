import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        import app as app_module
        app_module.current_name = None
        yield client


def test_get_greeting_without_post(client):
    response = client.get("/greeting")
    assert response.status_code == 200
    assert response.get_json() == {"greeting": "Hello, stranger!"}


def test_post_greeting_sets_name(client):
    response = client.post("/greeting", json={"name": "Alice"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Name 'Alice' saved"}


def test_get_greeting_after_post(client):
    client.post("/greeting", json={"name": "Alice"})
    response = client.get("/greeting")
    assert response.status_code == 200
    assert response.get_json() == {"greeting": "Hello, Alice!"}


def test_post_greeting_updates_name(client):
    client.post("/greeting", json={"name": "Alice"})
    client.post("/greeting", json={"name": "Bob"})
    response = client.get("/greeting")
    assert response.status_code == 200
    assert response.get_json() == {"greeting": "Hello, Bob!"}


def test_post_greeting_missing_name(client):
    response = client.post("/greeting", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "name is required"}


def test_post_greeting_no_body(client):
    response = client.post("/greeting", content_type="application/json", data="")
    assert response.status_code == 400
