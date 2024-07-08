import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel

from src.database import get_db
from src.main import app

client = TestClient(app)


class MockSession:
    def __init__(self):
        self.users = []

    def add(self, user):
        self.users.append(user)

    def commit(self):
        pass

    def rollback(self):
        pass


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


# Test successful signup
def test_signup_success(client_with_db):
    test_payload = {"username": "sophie_test", "password": "Sophietest123"}
    response = client_with_db.post("/api/v1/signup", json=test_payload)
    assert response.status_code == 201
    assert response.json() == {"success": True, "reason": "User created successfully"}


# Test password validation error (no uppercase letter)
def test_signup_password_no_uppercase(client_with_db):
    test_payload = {"username": "testuser", "password": "testpassword123"}
    response = client_with_db.post("/api/v1/signup", json=test_payload)
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Password must contain at least 1 uppercase letter, 1 lowercase letter and at least 1 number",  # noqa: E501
    }


# Test password validation error (no uppercase letter)
def test_signup_password_no_lowercase(client_with_db):
    test_payload = {"username": "testuser", "password": "TESTPASSWORD123"}
    response = client_with_db.post("/api/v1/signup", json=test_payload)
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Password must contain at least 1 uppercase letter, 1 lowercase letter and at least 1 number",  # noqa: E501
    }


# Test password validation error (no number)
def test_signup_password_no_number(client_with_db):
    test_payload = {"username": "testuser", "password": "Testpassword"}
    response = client_with_db.post("/api/v1/signup", json=test_payload)
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Password must contain at least 1 uppercase letter, 1 lowercase letter and at least 1 number",  # noqa: E501
    }


# Test password validation error (too short)
def test_signup_password_validation_too_short(client_with_db):
    response = client_with_db.post(
        "/api/v1/signup", json={"username": "testuser", "password": "Test1"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Ensure the length of password should be in a property range",
    }


# Test password validation error (too long)
def test_signup_password_validation_too_long(client_with_db):
    response = client_with_db.post(
        "/api/v1/signup", json={"username": "testuser", "password": "T" * 33 + "1aA"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Ensure the length of password should be in a property range",
    }


# Test username validation error (too short)
def test_signup_username_validation_too_short(client_with_db):
    response = client_with_db.post(
        "/api/v1/signup", json={"username": "us", "password": "Testpass123"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Ensure the length of username should be in a property range",
    }


# Test username validation error (too long)
def test_signup_username_validation_too_long(client_with_db):
    response = client_with_db.post(
        "/api/v1/signup", json={"username": "u" * 33, "password": "Testpass123"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "success": False,
        "reason": "Ensure the length of username should be in a property range",
    }
