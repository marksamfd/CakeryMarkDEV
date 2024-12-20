import pytest
from app.db import create_app, db
from app.Repositories.auth_repository import AuthRepository
from app.models import CustomerUser, Cart
from datetime import datetime, timezone

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    # Use an in-memory SQLite database for testing
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def auth_repo():
    return AuthRepository()

def test_add_user_success(auth_repo, test_app):
    with test_app.app_context():
        user_data = {
            "email": "testuser@gmail.com",
            "password": "testpassword",
            "firstname": "Test",
            "lastname": "User",
            "phonenum": "123456789",
            "addressgooglemapurl": "http://maps.example.com",
            "createdat": datetime.now(timezone.utc)
        }

        response, status_code = auth_repo.add_user(user_data)

        assert status_code == 201
        assert response["status"] == "success"
        assert "User signed up successfully" in response["message"]

        # Verify the user exists in the database
        user = CustomerUser.query.filter_by(customeremail="testuser@gmail.com").first()
        assert user is not None
        assert user.firstname == "Test"

        # Verify the cart is created
        cart = Cart.query.filter_by(customeremail="testuser@gmail.com").first()
        assert cart is not None

def test_add_user_existing_email(auth_repo, test_app):
    with test_app.app_context():
        user_data = {
            "email": "testuser@gmail.com",  # Already exists
            "password": "newpassword",
            "firstname": "Duplicate",
            "lastname": "User",
            "phonenum": "987654321",
            "addressgooglemapurl": "http://maps.example.com",
            "createdat": datetime.now(timezone.utc)
        }

        response, status_code = auth_repo.add_user(user_data)

        assert status_code == 409
        assert response["status"] == "error"
        assert "User already exists with this email" in response["message"]

def test_add_user_missing_fields(auth_repo, test_app):
    with test_app.app_context():
        user_data = {
            "email": "missingfields@gmail.com",
            "password": "testpassword",
            # Missing firstname
            "lastname": "User",
            "phonenum": "123456789",
            "addressgooglemapurl": "http://maps.example.com",
        }

        response, status_code = auth_repo.add_user(user_data)

        assert status_code == 400
        assert response["status"] == "error"
        assert "Missing required fields" in response["message"]

def test_user_sign_in_success(auth_repo, test_app):
    with test_app.app_context():
        login_data = {
            "email": "testuser@gmail.com",
            "password": "testpassword"
        }

        response, status_code = auth_repo.user_sign_in(login_data)

        assert status_code == 200
        assert response["status"] == "success"
        assert "access_token" in response

def test_user_sign_in_invalid_email(auth_repo, test_app):
    with test_app.app_context():
        login_data = {
            "email": "invalid@unknown.com",
            "password": "somepassword"
        }

        response, status_code = auth_repo.user_sign_in(login_data)

        assert status_code == 400
        assert response["status"] == "error"
        assert "Invalid email domain" in response["message"]

def test_user_sign_in_non_existent(auth_repo, test_app):
    with test_app.app_context():
        login_data = {
            "email": "nonexistent@gmail.com",
            "password": "somepassword"
        }

        response, status_code = auth_repo.user_sign_in(login_data)

        assert status_code == 401
        assert response["status"] == "error"
        assert "User not found" in response["message"]
