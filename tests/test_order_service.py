import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from app.Services.order_service import OrderService


@pytest.fixture(scope="function")
def order_service():
    """
    Fixture to initialize the OrderService with mocked repositories.
    """
    order_service = OrderService()
    order_service.order_repo = MagicMock()
    order_service.delivery_repo = MagicMock()
    return order_service


def test_create_order_from_cart(order_service):
    """
    Test the create_order_from_cart method.
    """
    # Arrange
    customer_email = "test@example.com"
    cart_items = [{"productid": 1, "quantity": 2, "price": 20.0}]
    voucher_code = "DISCOUNT10"
    expected_response = {"message": "Order created successfully", "order_id": 123}

    order_service.order_repo.create_order.return_value = expected_response

    # Act
    result = order_service.create_order_from_cart(customer_email, cart_items, voucher_code)

    # Assert
    order_service.order_repo.create_order.assert_called_once_with(
        customer_email, cart_items, voucher_code
    )
    assert result == expected_response


def test_update_order_status(order_service):
    """
    Test the update_order_status method.
    """
    # Arrange
    order_id = 123
    status = "Delivered"
    expected_response = {"message": "Order status updated to Delivered"}

    order_service.order_repo.update_order_status.return_value = expected_response

    # Act
    result = order_service.update_order_status(order_id, status)

    # Assert
    order_service.order_repo.update_order_status.assert_called_once_with(order_id, status)
    assert result == expected_response


def test_assign_delivery(order_service):
    """
    Test the assign_delivery method.
    """
    # Arrange
    order_id = 123
    expected_response = {"message": "Order assigned to delivery user"}

    order_service.delivery_repo.assign_delivery_user.return_value = expected_response

    # Act
    result = order_service.assign_delivery(order_id)

    # Assert
    order_service.delivery_repo.assign_delivery_user.assert_called_once_with(order_id)
    assert result == expected_response
