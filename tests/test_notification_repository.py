import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.db import create_app, db
from app.Repositories.notification_repository import NotificationRepository
from app.models import Notification, CustomerUser


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
def notification_repo():
    """
    Instantiates the NotificationRepository.
    """
    return NotificationRepository()


# Helper function to populate test data
def populate_test_data():
    """
    Populate the database with test data.
    """
    # Add customers
    customer = CustomerUser(
        customeremail="customer1@example.com",
        firstname="John",
        lastname="Doe",
        password="password123",
        phonenum="123456789",
    )
    db.session.add(customer)
    db.session.commit()


def test_save_notification_success(notification_repo, test_app):
    """
    Test successful saving of a notification to the database.
    """
    with test_app.app_context():
        populate_test_data()

        response = notification_repo.save_notification(
            customer_email="customer1@example.com", message="Your order has been shipped."
        )

        assert "message" in response
        assert response["message"] == "notification saved"

        # Verify the notification is saved in the database
        notification = Notification.query.filter_by(customer_email="customer1@example.com").first()
        assert notification is not None
        assert notification.message == "Your order has been shipped."


def test_save_notification_invalid_customer(notification_repo, test_app):
    """
    Test saving a notification for a non-existent customer.
    """
    with test_app.app_context():
        response = notification_repo.save_notification(
            customer_email="invalid_customer@example.com", message="Notification for invalid customer."
        )

        assert "error" in response
        assert "Customer with email invalid_customer@example.com does not exist." in response["error"]


        # Ensure no notification is saved in the database
        notification = Notification.query.filter_by(customer_email="invalid_customer@example.com").first()
        assert notification is None


def test_save_multiple_notifications(notification_repo, test_app):
    """
    Test saving multiple notifications for the same customer.
    """
    with test_app.app_context():
        populate_test_data()

        # Save the first notification
        response1 = notification_repo.save_notification(
            customer_email="customer1@example.com", message="Your order has been processed."
        )
        assert "message" in response1
        assert response1["message"] == "notification saved"

        # Save the second notification
        response2 = notification_repo.save_notification(
            customer_email="customer1@example.com", message="Your order has been delivered."
        )
        assert "message" in response2
        assert response2["message"] == "notification saved"

        # Verify both notifications are saved
        notifications = Notification.query.filter_by(customer_email="customer1@example.com").all()
        assert len(notifications) == 2
        assert notifications[0].message == "Your order has been processed."
        assert notifications[1].message == "Your order has been delivered."
