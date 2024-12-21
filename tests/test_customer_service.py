import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.Services.customer_service import CustomerService
from unittest.mock import MagicMock


@pytest.fixture(scope="function")
def customer_service():
    """
    Create a CustomerService instance with mocked dependencies.
    """
    service = CustomerService()
    service.customer_repo = MagicMock()
    service.order_repo = MagicMock()
    return service


def test_list_products_success(customer_service):
    """
    Test listing all products.
    """
    mock_products = [
        {"product_id": 1, "name": "Chocolate Cake", "price": 25.00},
        {"product_id": 2, "name": "Vanilla Cake", "price": 20.00},
    ]
    customer_service.customer_repo.get_all_products.return_value = mock_products
    response = customer_service.list_products()
    assert response == mock_products
    customer_service.customer_repo.get_all_products.assert_called_once()


def test_view_product_details_success(customer_service):
    """
    Test viewing details of a specific product.
    """
    mock_product = {"product_id": 1, "name": "Chocolate Cake", "price": 25.00}
    customer_service.customer_repo.get_product_by_id.return_value = mock_product
    response = customer_service.view_product_details(1)
    assert response == mock_product
    customer_service.customer_repo.get_product_by_id.assert_called_once_with(1)


def test_view_cart_success(customer_service):
    """
    Test viewing the cart.
    """
    mock_cart = {
        "cart_id": 1,
        "items": [{"product_id": 1, "quantity": 2, "price": 25.00}],
    }
    customer_service.customer_repo.get_cart.return_value = mock_cart
    response = customer_service.view_cart("customer@example.com")
    assert response == mock_cart
    customer_service.customer_repo.get_cart.assert_called_once_with("customer@example.com")


def test_add_to_cart_success(customer_service):
    """
    Test adding an item to the cart.
    """
    customer_service.customer_repo.add_item_to_cart.return_value = {
        "message": "Item added to cart successfully"
    }
    response = customer_service.add_to_cart(
        "customer@example.com", 1, 2, None
    )
    assert response["message"] == "Item added to cart successfully"
    customer_service.customer_repo.add_item_to_cart.assert_called_once_with(
        "customer@example.com", 1, 2, None
    )


def test_remove_from_cart_success(customer_service):
    """
    Test removing an item from the cart.
    """
    customer_service.customer_repo.remove_from_cart.return_value = {
        "message": "Item removed from cart successfully"
    }
    response = customer_service.remove_from_cart("customer@example.com", 1)
    assert response["message"] == "Item removed from cart successfully"
    customer_service.customer_repo.remove_from_cart.assert_called_once_with(
        "customer@example.com", 1
    )


def test_checkout_success(customer_service):
    """
    Test successfully checking out.
    """
    mock_cart = {
        "cart_id": 1,
        "items": [{"product_id": 1, "quantity": 2, "price": 25.00}],
    }
    mock_order = {"message": "Order created successfully", "order_id": 1}
    customer_service.customer_repo.get_cart.return_value = mock_cart
    customer_service.order_repo.create_order.return_value = mock_order

    response = customer_service.checkout("customer@example.com", "DISCOUNT10")
    assert response == mock_order
    customer_service.customer_repo.get_cart.assert_called_once_with("customer@example.com")
    customer_service.order_repo.create_order.assert_called_once_with(
        "customer@example.com", mock_cart["items"], "DISCOUNT10"
    )


def test_checkout_cart_not_found(customer_service):
    """
    Test checkout when the cart is not found.
    """
    customer_service.customer_repo.get_cart.return_value = {"error, cart not found": "Cart not found"}
    response = customer_service.checkout("customer@example.com", "DISCOUNT10")
    assert response["error, cart not found"] == "Cart not found"
    customer_service.customer_repo.get_cart.assert_called_once_with("customer@example.com")


def test_view_notifications_success(customer_service):
    """
    Test viewing notifications for a customer.
    """
    mock_notifications = [
        {"id": 1, "message": "Order shipped"},
        {"id": 2, "message": "Order delivered"},
    ]
    customer_service.customer_repo.get_notifications.return_value = mock_notifications
    response = customer_service.view_notifications("customer@example.com")
    assert response == mock_notifications
    customer_service.customer_repo.get_notifications.assert_called_once_with("customer@example.com")


def test_increment_quantity_success(customer_service):
    """
    Test incrementing the quantity of a cart item.
    """
    customer_service.customer_repo.increment_quantity.return_value = {
        "message": "Quantity updated successfully",
        "new_quantity": 2,
    }
    data = {"product_id": 1, "action": "increment"}
    response = customer_service.incrementQuantity(data, "customer@example.com")
    assert response["message"] == "Quantity updated successfully"
    assert response["new_quantity"] == 2
    customer_service.customer_repo.increment_quantity.assert_called_once_with(
        "customer@example.com", data["product_id"], data["action"]
    )


def test_add_review_success(customer_service):
    """
    Test successfully adding a review for a product.
    """
    customer_service.customer_repo.place_review.return_value = {
        "message": "Review added successfully"
    }
    response = customer_service.add_review("customer@example.com", 5, 1)
    assert response["message"] == "Review added successfully"
    customer_service.customer_repo.place_review.assert_called_once_with(
        "customer@example.com", 5, 1
    )
