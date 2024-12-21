
import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from app.Services.delivery_service import DeliveryService


@pytest.fixture(scope="function")
def delivery_service():
    """
    Create a DeliveryService instance with mocked dependencies.
    """
    notifier = MagicMock()
    service = DeliveryService(notifier=notifier)
    service.delivery_repo = MagicMock()
    service.order_repo = MagicMock()
    service.otp_service = MagicMock()
    return service


def test_mark_order_status_delivered_success(delivery_service):
    """
    Test marking an order status as 'delivered' successfully.
    """
    order_id = 1
    customer_email = "customer@example.com"
    otp_code = "123456"

    delivery_service.order_repo.update_order_status.return_value = {"message": "Order status updated"}
    delivery_service.order_repo.get_customerEmail_by_order_id.return_value = customer_email
    delivery_service.otp_service.generate_and_save_otp.return_value = otp_code

    response = delivery_service.mark_order_status(order_id, "delivered")

    assert response == "Order status updated successfully"
    delivery_service.order_repo.update_order_status.assert_called_once_with(order_id, "delivered")
    delivery_service.order_repo.get_customerEmail_by_order_id.assert_called_once_with(order_id)
    delivery_service.otp_service.generate_and_save_otp.assert_called_once_with(customer_email, order_id)


def test_mark_order_status_out_for_delivery_success(delivery_service):
    """
    Test marking an order status as 'out_for_delivery' successfully.
    """
    order_id = 2
    customer_email = "customer@example.com"

    delivery_service.order_repo.update_order_status.return_value = {"message": "Order status updated"}
    delivery_service.order_repo.get_customerEmail_by_order_id.return_value = customer_email

    response = delivery_service.mark_order_status(order_id, "out_for_delivery")

    assert response == "Order status updated successfully"
    delivery_service.order_repo.update_order_status.assert_called_once_with(order_id, "out_for_delivery")
    delivery_service.order_repo.get_customerEmail_by_order_id.assert_called_once_with(order_id)
    delivery_service.notifier.notify_observers.assert_called_once_with(customer_email, "Your order is out for delivery")


def test_mark_order_status_invalid_status(delivery_service):
    """
    Test marking an order status with an invalid status.
    """
    order_id = 3
    invalid_status = "unknown_status"

    response = delivery_service.mark_order_status(order_id, invalid_status)

    assert response["error"] == f"Order status cant' be updated to this status , status: {invalid_status}"
    delivery_service.order_repo.update_order_status.assert_not_called()


def test_view_assigned_orders_success(delivery_service):
    """
    Test viewing assigned orders for a delivery user.
    """
    delivery_email = "delivery@example.com"
    mock_orders = [
        {"order_id": 1, "status": "Pending"},
        {"order_id": 2, "status": "Out for Delivery"},
    ]

    delivery_service.delivery_repo.get_assigned_orders.return_value = mock_orders
    response = delivery_service.view_assigned_orders(delivery_email)

    assert response == mock_orders
    delivery_service.delivery_repo.get_assigned_orders.assert_called_once_with(delivery_email)


def test_get_deliveryman_name_success(delivery_service):
    """
    Test retrieving the name of a deliveryman.
    """
    delivery_email = "delivery@example.com"
    deliveryman_name = "John Doe"

    delivery_service.delivery_repo.get_deliveryman_name.return_value = deliveryman_name
    response = delivery_service.get_deliveryman_name(delivery_email)

    assert response == deliveryman_name
    delivery_service.delivery_repo.get_deliveryman_name.assert_called_once_with(delivery_email)


def test_mark_order_status_error_generating_otp(delivery_service):
    """
    Test error while generating OTP during 'delivered' status update.
    """
    order_id = 1
    customer_email = "customer@example.com"

    delivery_service.order_repo.update_order_status.return_value = {"message": "Order status updated"}
    delivery_service.order_repo.get_customerEmail_by_order_id.return_value = customer_email
    delivery_service.otp_service.generate_and_save_otp.return_value = None

    response = delivery_service.mark_order_status(order_id, "delivered")

    assert response["error"] == "Error generating OTP"
    delivery_service.order_repo.update_order_status.assert_called_once_with(order_id, "delivered")
    delivery_service.order_repo.get_customerEmail_by_order_id.assert_called_once_with(order_id)
    delivery_service.otp_service.generate_and_save_otp.assert_called_once_with(customer_email, order_id)
