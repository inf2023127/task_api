import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "username": "test",
            "title": "Test Task",
            "description": "Testing",
            "deadline": "2026-01-30"
        }
    )
    assert response.status_code == 201


def test_get_task_by_id(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200


def test_delete_task(client):
    response = client.delete("/tasks/1")
    assert response.status_code == 200