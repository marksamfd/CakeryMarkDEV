import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.Services.auth_service import AuthService
from unittest.mock import MagicMock


@pytest.fixture(scope="function")
def auth_service():
    """
    Create an AuthService instance with mocked dependencies.
    """
    service = AuthService()
    service.auth_repo = MagicMock()
    return service


def test_add_new_user_success(auth_service):
    """
    Test successfully adding a new user.
    """
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@example.com",
        "password": "securepassword123",
        "role": "customer",
    }
    auth_service.auth_repo.add_user.return_value = {"message": "User added successfully"}
    response = auth_service.add_new_user(data)
    assert response["message"] == "User added successfully"
    auth_service.auth_repo.add_user.assert_called_once_with(data)


def test_add_new_user_failure(auth_service):
    """
    Test failing to add a new user due to missing data.
    """
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "",
        "password": "securepassword123",
        "role": "customer",
    }
    auth_service.auth_repo.add_user.return_value = {"error": "Email is required"}
    response = auth_service.add_new_user(data)
    assert response["error"] == "Email is required"
    auth_service.auth_repo.add_user.assert_called_once_with(data)


def test_sign_user_in_success(auth_service):
    """
    Test successfully signing in a user.
    """
    data = {
        "email": "john@example.com",
        "password": "securepassword123",
    }
    auth_service.auth_repo.user_sign_in.return_value = {
        "message": "Sign-in successful",
        "token": "some-jwt-token",
    }
    response = auth_service.sign_user_in(data)
    assert response["message"] == "Sign-in successful"
    assert "token" in response
    auth_service.auth_repo.user_sign_in.assert_called_once_with(data)


def test_sign_user_in_invalid_credentials(auth_service):
    """
    Test signing in with invalid credentials.
    """
    data = {
        "email": "john@example.com",
        "password": "wrongpassword",
    }
    auth_service.auth_repo.user_sign_in.return_value = {
        "error": "Invalid credentials"
    }
    response = auth_service.sign_user_in(data)
    assert response["error"] == "Invalid credentials"
    auth_service.auth_repo.user_sign_in.assert_called_once_with(data)
