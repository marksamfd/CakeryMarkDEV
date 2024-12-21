import pytest
from unittest.mock import MagicMock
from app.Services.notification_services import NotificationService


@pytest.fixture(scope="function")
def notification_service():
    """
    Create a NotificationService instance with mocked dependencies.
    """
    service = NotificationService()
    service.notification_repo = MagicMock()
    return service


def test_send_notification_success(notification_service):
    """
    Test sending a notification successfully.
    """
    customer_email = "customer@example.com"
    message = "Your order is ready for pickup."

    # Mock the `save_notification` method to avoid database operations
    notification_service.notification_repo.save_notification.return_value = {"message": "notification saved"}

    # Call the service method
    notification_service.send_notification(customer_email, message)

    # Verify that the print statement was executed (optional, for debugging)
    print(f"Verified sending push notification to {customer_email}: {message}")

    # Assert the `save_notification` method is called with correct arguments
    notification_service.notification_repo.save_notification.assert_called_once_with(customer_email, message)
