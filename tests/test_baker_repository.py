import sys
import os

# Add the parent directory of 'app' to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app.db import create_app, db
from app.models import Orders, Inventory, CustomizeCake, OrderItems, CustomerUser, DeliveryUser
from app.Repositories.baker_repository import BakerRepository

@pytest.fixture(scope="function")
def test_app():
    """
    Creates a Flask application configured for testing.
    Uses an in-memory SQLite database.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Adjust as needed
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()  # Create all tables
        yield app
        db.session.remove()

        # Rollback all changes made during the test
        db.session.rollback()

@pytest.fixture(scope="function")
def baker_repo():
    """
    Instantiates the BakerRepository.
    """
    return BakerRepository()

def populate_test_data():
    """
    Populate the database with test data.
    Checks for existing records to avoid duplicate key errors.
    """
    # Check or create customer
    customer = CustomerUser.query.filter_by(customeremail="customer99@example.com").first()
    if not customer:
        customer = CustomerUser(customeremail="customer99@example.com", firstname="John", password="1234")
        db.session.add(customer)

    # Check or create delivery user
    delivery_user = DeliveryUser.query.filter_by(deliveryemail="delivery99@example.com").first()
    if not delivery_user:
        delivery_user = DeliveryUser(deliveryemail="delivery99@example.com", firstname="Jane", password="45678")
        db.session.add(delivery_user)

    # Add inventory item if not present
    inventory_item = Inventory.query.filter_by(name="Chocolate vanilla Cakee").first()
    if not inventory_item:
        inventory_item = Inventory(
            name="Chocolate vanilla Cakee",
            description="Delicious chocolate cake",
            price=25.00,
            category="Cakes"
        )
        db.session.add(inventory_item)

    # Add a custom cake
    custom_cake = CustomizeCake.query.filter_by(customeremail=customer.customeremail).first()
    if not custom_cake:
        custom_cake = CustomizeCake(
            numlayers=3,
            customeremail=customer.customeremail,
            cakeshape="Round",
            cakesize="Medium",
            cakeflavor="Vanilla",
            message="Happy Birthday",
            price=75.00
        )
        db.session.add(custom_cake)

    # Add an order
    order = Orders.query.filter_by(customeremail=customer.customeremail).first()
    if not order:
        order = Orders(
            customeremail=customer.customeremail,
            deliveryemail=delivery_user.deliveryemail,
            totalprice=100.00,
            status="Pending"
        )
        db.session.add(order)

    # Add order item
    order_item = OrderItems.query.filter_by(orderid=order.orderid).first()
    if not order_item:
        order_item = OrderItems(
            orderid=order.orderid,
            productid=inventory_item.productid,
            customizecakeid=custom_cake.customizecakeid,
            quantity=2,
            priceatorder=50.00
        )
        db.session.add(order_item)

    db.session.commit()


def test_get_all_orders_success(baker_repo, test_app):
    with test_app.app_context():
        populate_test_data()
        response = baker_repo.get_all_orders()

        assert isinstance(response, list)
        assert len(response) > 0
        assert "orderID" in response[0]
        assert "customer" in response[0]
        assert "email" in response[0]["customer"]


def test_get_order_details_success(baker_repo, test_app):
    with test_app.app_context():
        populate_test_data()
        order = Orders.query.first()
        response = baker_repo.get_order_details(order.orderid)

        assert "orderID" in response
        assert response["orderID"] == order.orderid
        assert response["status"] == order.status
        assert response["customeremail"] == order.customeremail

def test_get_order_details_not_found(baker_repo, test_app):
    """
    Test retrieval of order details for a non-existent order.
    """
    with test_app.app_context():
        response = baker_repo.get_order_details(99)

        assert "error" in response
        assert response["error"] == "Order not found"

def test_update_order_status_success(baker_repo, test_app):
    with test_app.app_context():
        populate_test_data()
        order = Orders.query.first()
        response = baker_repo.update_order_status(order.orderid, "Prepared")

        assert "message" in response
        assert response["message"] == "Order status updated to Prepared"

        updated_order = Orders.query.get(order.orderid)
        assert updated_order.status == "Prepared"


def test_update_order_status_not_found(baker_repo, test_app):
    with test_app.app_context():
        response = baker_repo.update_order_status(999, "delivered")

        assert "error" in response
        assert response["error"] == "Order not found"