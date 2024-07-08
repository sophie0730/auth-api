import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from src.database import get_db
from src.main import app

client = TestClient(app)

users = {}


class MockSession:
    def __init__(self):
        self.users = users

    def add(self, user):
        self.users[user.username] = user

    def commit(self):
        pass

    def rollback(self):
        pass

    def query(self, model):
        self.query_model = model
        return self

    def filter(self, condition):
        username = condition.right.value
        if username in self.users:
            self.filtered_user = self.users[username]
        else:
            self.filtered_user = None
        return self

    def first(self):
        return self.filtered_user


class ValidUser(BaseModel):
    username: str
    password: str


def mock_get_db():
    return MockSession()


@pytest.fixture
def client_with_db():
    app.dependency_overrides[get_db] = mock_get_db
    yield client
    app.dependency_overrides = {}


@pytest.fixture
def mock_redis():
    with patch("src.auth.rate_limiter.redis_client") as mock_redis_client:
        yield mock_redis_client


def test_signin_successful(client_with_db, mock_redis):
    test_payload = {"username": "testuser", "password": "Testuser123"}
    mock_redis.exists.return_value = False

    client_with_db.post("/api/v1/signup", json=test_payload)

    response = client_with_db.post("/api/v1/signin", json=test_payload)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"success": True, "reason": "User sign in successfully"}
    mock_redis.setex.assert_not_called()


def test_signin_user_does_not_exist(client_with_db, mock_redis):
    test_payload = {"username": "nonexistentuser", "password": "Testuser123"}
    mock_redis.exists.return_value = False

    response = client_with_db.post("/api/v1/signin", json=test_payload)
    assert response.status_code == 404
    assert response.json()["reason"] == "The username doesn't exist"
    mock_redis.setex.assert_not_called()


def test_signin_wrong_password(client_with_db, mock_redis):
    existing_user = {"username": "testuser", "password": "Wrongpassword123"}
    mock_redis.exists.return_value = False
    client_with_db.post(
        "/api/v1/signup", json={"username": "testuser", "password": "correctpassword"}
    )

    response = client_with_db.post("/api/v1/signin", json=existing_user)
    assert response.status_code == 400
    assert response.json()["reason"] == "The password is wrong"
    mock_redis.setex.assert_not_called()