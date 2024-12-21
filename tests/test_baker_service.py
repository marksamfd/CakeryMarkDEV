import pytest
from app.Services.baker_service import BakerService
from unittest.mock import MagicMock


@pytest.fixture(scope="function")
def baker_service():
    """
    Create a BakerService instance with mocked dependencies.
    """
    service = BakerService()
    service.baker_repo = MagicMock()
    service.order_service = MagicMock()
    return service


def test_view_baker_orders_success(baker_service):
    """
    Test successful retrieval of all orders for the baker.
    """
    mock_orders = [
        {"orderID": 1, "status": "Pending", "totalPrice": 50.0},
        {"orderID": 2, "status": "Prepared", "totalPrice": 75.0},
    ]
    baker_service.baker_repo.get_all_orders.return_value = mock_orders
    response = baker_service.view_baker_orders()
    assert response == mock_orders
    baker_service.baker_repo.get_all_orders.assert_called_once()


def test_view_specific_order_success(baker_service):
    """
    Test successful retrieval of a specific order.
    """
    mock_order = {
        "orderID": 1,
        "status": "Pending",
        "items": [{"productID": 101, "quantity": 2}],
    }
    baker_service.baker_repo.get_order_details.return_value = mock_order
    response = baker_service.view_specific_order(1)
    assert response == mock_order
    baker_service.baker_repo.get_order_details.assert_called_once_with(1)


def test_view_specific_order_not_found(baker_service):
    """
    Test retrieval of a non-existent order.
    """
    baker_service.baker_repo.get_order_details.return_value = None
    response = baker_service.view_specific_order(999)
    assert response is None
    baker_service.baker_repo.get_order_details.assert_called_once_with(999)


def test_mark_order_prepared_success(baker_service):
    """
    Test successfully marking an order as prepared and assigning a delivery user.
    """
    baker_service.baker_repo.update_order_status.return_value = {
        "message": "Order status updated to Prepared"
    }
    baker_service.order_service.assign_delivery.return_value = {
        "message": "Order assigned to delivery user"
    }
    response = baker_service.mark_order_prepared(1)
    assert response["message"] == "Order assigned to delivery user"
    baker_service.baker_repo.update_order_status.assert_called_once_with(1, "Prepared")
    baker_service.order_service.assign_delivery.assert_called_once_with(1)


def test_mark_order_prepared_failure_update(baker_service):
    """
    Test failure when marking an order as prepared fails.
    """
    baker_service.baker_repo.update_order_status.return_value = {
        "error": "Order not found"
    }
    response = baker_service.mark_order_prepared(1)
    assert response["error"] == "Order not found"
    baker_service.baker_repo.update_order_status.assert_called_once_with(1, "Prepared")
    baker_service.order_service.assign_delivery.assert_not_called()


def test_mark_order_prepared_failure_assignment(baker_service):
    """
    Test failure during delivery assignment after marking order as prepared.
    """
    baker_service.baker_repo.update_order_status.return_value = {
        "message": "Order status updated to Prepared"
    }
    baker_service.order_service.assign_delivery.return_value = {
        "error": "No delivery users available"
    }
    response = baker_service.mark_order_prepared(1)
    assert response["error"] == "No delivery users available"
    baker_service.baker_repo.update_order_status.assert_called_once_with(1, "Prepared")
    baker_service.order_service.assign_delivery.assert_called_once_with(1)
