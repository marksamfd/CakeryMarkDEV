import pytest
from app.db import create_app, db
from app.Repositories.auth_repository import AuthRepository
from app.models import CustomerUser, Cart
from datetime import datetime, timezone
from unittest.mock import patch

# Fixture to create the test app
@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()  # Create all tables
        yield app
        db.drop_all()  # Drop all tables after tests are done
    print(app.config['SQLALCHEMY_DATABASE_URI'])


# Fixture for AuthRepository
@pytest.fixture(scope='module')
def auth_repo():
    return AuthRepository()

# Fixture to clean the database between tests
@pytest.fixture(scope='function')
def clean_db(test_app):
    with test_app.app_context():
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

# Test cases
def test_add_user_success(auth_repo, test_app, clean_db):
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

        assert status_code == 201, f"Expected 201, got {status_code}"
        assert response["status"] == "success"
        assert "User signed up successfully" in response["message"]

        user = CustomerUser.query.filter_by(customeremail="testuser@gmail.com").first()
        assert user is not None
        assert user.firstname == "Test"

        cart = Cart.query.filter_by(customeremail="testuser@gmail.com").first()
        assert cart is not None

def test_add_user_existing_email(auth_repo, test_app, clean_db):
    with test_app.app_context():
        # Add initial user
        user_data = {
            "email": "testuser@gmail.com",
            "password": "testpassword",
            "firstname": "Test",
            "lastname": "User",
            "phonenum": "123456789",
            "addressgooglemapurl": "http://maps.example.com",
            "createdat": datetime.now(timezone.utc)
        }
        auth_repo.add_user(user_data)

        # Try adding a duplicate user
        duplicate_data = {
            "email": "testuser@gmail.com",
            "password": "newpassword",
            "firstname": "Duplicate",
            "lastname": "User",
            "phonenum": "987654321",
            "addressgooglemapurl": "http://maps.example.com",
            "createdat": datetime.now(timezone.utc)
        }

        response, status_code = auth_repo.add_user(duplicate_data)

        assert status_code == 409, f"Expected 409, got {status_code}"
        assert response["status"] == "error"
        assert "User already exists with this email" in response["message"]

def test_add_user_missing_fields(auth_repo, test_app, clean_db):
    with test_app.app_context():
        user_data = {
            "email": "missingfields@gmail.com",
            "password": "testpassword",
            "lastname": "User",
            "phonenum": "123456789",
            "addressgooglemapurl": "http://maps.example.com",
        }

        response, status_code = auth_repo.add_user(user_data)

        assert status_code == 400, f"Expected 400, got {status_code}"
        assert response["status"] == "error"
        assert "Missing required fields" in response["message"]

def test_add_user_invalid_email_format(auth_repo, test_app, clean_db):
    with test_app.app_context():
        user_data = {
            "email": "invalid-email",
            "password": "testpassword",
            "firstname": "Invalid",
            "lastname": "Email",
            "phonenum": "123456789",
            "addressgooglemapurl": "http://maps.example.com",
            "createdat": datetime.now(timezone.utc)
        }

        response, status_code = auth_repo.add_user(user_data)

        assert status_code == 400, f"Expected 400, got {status_code}"
        assert response["status"] == "error"
        assert "Invalid email format" in response["message"]

def test_user_sign_in_success(auth_repo, test_app, clean_db):
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
        auth_repo.add_user(user_data)

        login_data = {
            "email": "testuser@gmail.com",
            "password": "testpassword"
        }

        response, status_code = auth_repo.user_sign_in(login_data)

        assert status_code == 200, f"Expected 200, got {status_code}"
        assert response["status"] == "success"
        assert "access_token" in response

def test_user_sign_in_invalid_email(auth_repo, test_app, clean_db):
    with test_app.app_context():
        login_data = {
            "email": "invalid@unknown.com",
            "password": "somepassword"
        }

        response, status_code = auth_repo.user_sign_in(login_data)

        assert status_code == 400, f"Expected 400, got {status_code}"
        assert response["status"] == "error"
        assert "Invalid email domain" in response["message"]

def test_user_sign_in_non_existent(auth_repo, test_app, clean_db):
    with test_app.app_context():
        login_data = {
            "email": "nonexistent@gmail.com",
            "password": "somepassword"
        }

        response, status_code = auth_repo.user_sign_in(login_data)

        assert status_code == 401, f"Expected 401, got {status_code}"
        assert response["status"] == "error"
        assert "User not found" in response["message"]
