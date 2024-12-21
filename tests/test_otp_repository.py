import pytest
from datetime import datetime, timedelta, timezone
from app.db import create_app, db
from app.Repositories.otp_repository import OTPRepository
from app.models import OTP

@pytest.fixture(scope="function")
def test_app():
    """
    Creates a Flask application configured for testing.
    Uses an in-memory SQLite database.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def otp_repo():
    """
    Instantiates the OTPRepository.
    """
    return OTPRepository()

# Helper function to populate test data
def populate_test_data():
    """
    Populate the database with test data.
    """
    # Add OTP entries
    otp_valid = OTP(
        customer_email="customer1@example.com",
        otp_code="123456",
        expiry_time=datetime.now(timezone.utc) + timedelta(minutes=5),
        is_used=False,
    )
    otp_expired = OTP(
        customer_email="customer1@example.com",
        otp_code="654321",
        expiry_time=datetime.now(timezone.utc) - timedelta(minutes=5),  # Expired
        is_used=False,
    )
    db.session.add_all([otp_valid, otp_expired])
    db.session.commit()

def test_save_otp_success(otp_repo, test_app):
    """
    Test successful saving of an OTP to the database.
    """
    with test_app.app_context():
        otp_entry = otp_repo.save_otp(
            customer_email="customer1@example.com",
            otp_code="111111",
            expiry_time=datetime.now(timezone.utc) + timedelta(minutes=5),
            order_id=1,
        )
        assert otp_entry is not None
        assert otp_entry.customer_email == "customer1@example.com"
        assert otp_entry.otp_code == "111111"

def test_get_otp_success(otp_repo, test_app):
    """
    Test successful retrieval of an OTP.
    """
    with test_app.app_context():
        populate_test_data()
        otp_entry = otp_repo.get_otp("customer1@example.com", "123456")
        assert otp_entry is not None
        assert otp_entry.otp_code == "123456"

def test_get_otp_invalid(otp_repo, test_app):
    """
    Test retrieving an OTP with invalid details.
    """
    with test_app.app_context():
        populate_test_data()
        otp_entry = otp_repo.get_otp("customer1@example.com", "000000")
        assert otp_entry is None

def test_verify_otp_expired(otp_repo, test_app):
    """
    Test verifying an expired OTP.
    """
    with test_app.app_context():
        populate_test_data()
        otp_entry = otp_repo.get_otp("customer1@example.com", "654321")
        assert otp_entry is not None
        assert otp_entry.expiry_time < datetime.now(timezone.utc)

def test_mark_otp_used(otp_repo, test_app):
    """
    Test marking an OTP as used.
    """
    with test_app.app_context():
        populate_test_data()
        otp_entry = otp_repo.get_otp("customer1@example.com", "123456")
        otp_repo.mark_otp_used(otp_entry)
        assert otp_entry.is_used is True
