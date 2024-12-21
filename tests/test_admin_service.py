import pytest
from app.Services.admin_service import AdminService
from unittest.mock import MagicMock

@pytest.fixture(scope="function")
def admin_service():
    """
    Create an AdminService instance with mocked dependencies.
    """
    service = AdminService()
    service.admin_repo = MagicMock()
    service.order_repo = MagicMock()
    return service


def test_get_users(admin_service):
    """
    Test retrieving staff users.
    """
    # Mock return value
    admin_service.admin_repo.get_staff_users.return_value = [
        {"firstname": "John", "lastname": "Doe", "role": "baker"},
        {"firstname": "Jane", "lastname": "Smith", "role": "delivery"},
    ]
    users = admin_service.get_users()
    assert len(users) == 2
    assert users[0]["role"] == "baker"
    admin_service.admin_repo.get_staff_users.assert_called_once()


def test_add_user_baker(admin_service):
    """
    Test adding a baker user.
    """
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@example.com",
        "phone": "123456789",
        "password": "password123",
        "role": "baker",
    }
    admin_service.admin_repo.add_bakery_user.return_value = {"message": "Baker added successfully"}
    response = admin_service.add_user(data)
    assert response["message"] == "Baker added successfully"
    admin_service.admin_repo.add_bakery_user.assert_called_once_with(
        "John", "Doe", "john@example.com", "123456789", "password123"
    )


def test_add_user_delivery(admin_service):
    """
    Test adding a delivery user.
    """
    data = {
        "firstname": "Jane",
        "lastname": "Smith",
        "email": "jane@example.com",
        "phone": "987654321",
        "password": "password123",
        "role": "delivery",
    }
    admin_service.admin_repo.add_delivery_user.return_value = {"message": "Delivery user added successfully"}
    response = admin_service.add_user(data)
    assert response["message"] == "Delivery user added successfully"
    admin_service.admin_repo.add_delivery_user.assert_called_once_with(
        "Jane", "Smith", "jane@example.com", "987654321", "password123"
    )


def test_add_user_invalid_role(admin_service):
    """
    Test adding a user with an invalid role.
    """
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@example.com",
        "phone": "123456789",
        "password": "password123",
        "role": "invalid_role",
    }
    response, status_code = admin_service.add_user(data)
    assert response == {"passed role is wrong, error in adding user (service)"}
    assert status_code == 400


def test_delete_user_baker(admin_service):
    """
    Test deleting a baker user.
    """
    data = {"role": "baker", "email": "baker@example.com"}
    admin_service.admin_repo.delete_baker_user.return_value = {"message": "Baker deleted successfully"}
    response = admin_service.delete_user(data)
    assert response["message"] == "Baker deleted successfully"
    admin_service.admin_repo.delete_baker_user.assert_called_once_with("baker@example.com")


def test_get_products(admin_service):
    """
    Test retrieving products and raw materials.
    """
    admin_service.admin_repo.prducts_rawMats.return_value = [
        {"id": 1, "name": "Chocolate Cake", "price": 25.0},
        {"id": 2, "name": "Vanilla Cupcake", "price": 3.0},
    ]

    products = admin_service.get_products()
    assert len(products) == 2
    assert products[0]["name"] == "Chocolate Cake"
    admin_service.admin_repo.prducts_rawMats.assert_called_once()


def test_add_voucher(admin_service):
    """
    Test adding a voucher.
    """
    data = {"voucher_code": "DISCOUNT10", "discount": 10}
    admin_service.admin_repo.add_voucher.return_value = {"message": "Voucher added successfully"}
    response = admin_service.add_voucher(data)
    assert response["message"] == "Voucher added successfully"
    admin_service.admin_repo.add_voucher.assert_called_once_with("DISCOUNT10", 10)


def test_dashboard_data(admin_service):
    """
    Test retrieving dashboard data.
    """
    admin_service.admin_repo.get_dashboard_data.return_value = {"orders": 100, "customers": 50}
    dashboard = admin_service.dashboard_data()
    assert dashboard["orders"] == 100
    assert dashboard["customers"] == 50
    admin_service.admin_repo.get_dashboard_data.assert_called_once()
