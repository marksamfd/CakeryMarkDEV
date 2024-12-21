import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.db import create_app, db
from app.Repositories.delivery_repository import DeliveryRepository
from app.models import DeliveryAssignments, Orders, OrderItems, DeliveryUser, CustomerUser

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
def delivery_repo():
    """
    Instantiates the DeliveryRepository.
    """
    return DeliveryRepository()

# Helper function to add test data
def populate_test_data():
    """
    Populate the database with test data.
    """
    # Add customers
    customer1 = CustomerUser(
        customeremail="customer1@example.com",
        firstname="John",
        lastname="Doe",
        password="password1",
        phonenum="123456789",
        addressgooglemapurl="http://maps.example.com/customer1"
    )
    customer2 = CustomerUser(
        customeremail="customer2@example.com",
        firstname="Jane",
        lastname="Smith",
        password="password2",
        phonenum="987654321",
        addressgooglemapurl="http://maps.example.com/customer2"
    )
    db.session.add_all([customer1, customer2])
    db.session.commit()

    # Add delivery users
    delivery1 = DeliveryUser(
        deliveryemail="delivery1@example.com",
        firstname="Delivery",
        lastname="One",
        password="password3",
        phonenum="555123456"
    )
    delivery2 = DeliveryUser(
        deliveryemail="delivery2@example.com",
        firstname="Delivery",
        lastname="Two",
        password="password4",
        phonenum="555987654"
    )
    db.session.add_all([delivery1, delivery2])
    db.session.commit()

    # Add orders
    order1 = Orders(
        orderid=1,
        customeremail="customer1@example.com",
        totalprice=50.00,
        status="Pending"
    )
    order2 = Orders(
        orderid=2,
        customeremail="customer2@example.com",
        totalprice=75.00,
        status="Out for Delivery",
        deliveryemail="delivery1@example.com"
    )
    db.session.add_all([order1, order2])
    db.session.commit()

    # Assign orders
    assignment = DeliveryAssignments(
        orderid=2,
        deliveryemail="delivery1@example.com"
    )
    db.session.add(assignment)
    db.session.commit()

def test_get_assigned_orders(delivery_repo, test_app):
    """
    Test retrieving all orders assigned to a delivery user.
    """
    with test_app.app_context():
        populate_test_data()
        orders = delivery_repo.get_assigned_orders("delivery1@example.com")
        assert len(orders) == 1
        assert orders[0]["customerName"] == "Jane Smith"
        assert orders[0]["phone"] == "987654321"
        assert orders[0]["price"] == 75.00

def test_find_available_delivery_user(delivery_repo, test_app):
    """
    Test finding the delivery user with the least assigned orders.
    """
    with test_app.app_context():
        populate_test_data()
        available_user = delivery_repo.find_available_delivery_user()
        assert available_user == "delivery2@example.com"

def test_assign_delivery_user_success(delivery_repo, test_app):
    """
    Test assigning a delivery user to an order.
    """
    with test_app.app_context():
        populate_test_data()
        response = delivery_repo.assign_delivery_user(1)
        assert "message" in response
        assert "assigned" in response["message"]
        assignment = DeliveryAssignments.query.filter_by(orderid=1).first()
        assert assignment is not None
        assert assignment.deliveryemail == "delivery2@example.com"

def test_assign_delivery_user_no_available_user(delivery_repo, test_app):
    """
    Test assigning a delivery user when no users are available.
    """
    with test_app.app_context():
        populate_test_data()
        # Assign all users
        delivery_repo.assign_delivery_user(1)
        delivery_repo.assign_delivery_user(2)
        # Try assigning another order
        order3 = Orders(
            orderid=3,
            customeremail="customer2@example.com",
            totalprice=100.00,
            status="Pending"
        )
        db.session.add(order3)
        db.session.commit()
        response = delivery_repo.assign_delivery_user(3)
        assert "error" in response
        assert response["error"] == "No available delivery users to assign the order"

def test_get_deliveryman_name(delivery_repo, test_app):
    """
    Test retrieving the full name of a delivery user by email.
    """
    with test_app.app_context():
        populate_test_data()
        name = delivery_repo.get_deliveryman_name("delivery1@example.com")
        assert name == "Delivery One"
