import pytest
from datetime import datetime, timedelta
from app.db import create_app, db
from app.Repositories.order_repository import OrderRepository
from app.models import Orders, OrderItems, Inventory, Voucher, Cart, CustomerUser, DeliveryAssignments

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
def order_repo():
    """
    Instantiates the OrderRepository.
    """
    return OrderRepository()

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
        password="password1",
        phonenum="123456789"
    )
    db.session.add(customer)

    # Add inventory items
    product1 = Inventory(
        productid=1,
        name="Chocolate Cake",
        price=20.00,
        category="Cakes"
    )
    product2 = Inventory(
        productid=2,
        name="Vanilla Cupcake",
        price=5.00,
        category="Cupcakes"
    )
    db.session.add_all([product1, product2])

    # Add a voucher
    voucher = Voucher(
        vouchercode="DISCOUNT10",
        discountpercentage=10
    )
    db.session.add(voucher)

    # Add a cart for the customer
    cart = Cart(customeremail="customer1@example.com")
    db.session.add(cart)
    db.session.commit()

def test_create_order_success(order_repo, test_app):
    """
    Test successful creation of an order.
    """
    with test_app.app_context():
        populate_test_data()

        cart_items = [
            {"productid": 1, "quantity": 2, "price": 20.00},
            {"productid": 2, "quantity": 4, "price": 5.00}
        ]

        response = order_repo.create_order(
            customer_email="customer1@example.com",
            cart_items=cart_items,
            voucher_code="DISCOUNT10"
        )

        assert "order_id" in response
        assert response["total_price"] == 63.0  # 20*2 + 5*4 = 70; 10% discount = 63
        assert len(response["items"]) == 2

def test_create_order_invalid_voucher(order_repo, test_app):
    """
    Test order creation with an invalid voucher code.
    """
    with test_app.app_context():
        populate_test_data()

        cart_items = [
            {"productid": 1, "quantity": 1, "price": 20.00},
        ]

        response = order_repo.create_order(
            customer_email="customer1@example.com",
            cart_items=cart_items,
            voucher_code="INVALIDCODE"
        )

        assert "error" in response
        assert "(repo) Invalid voucher code" in response["error"]

def test_get_orders_by_customer(order_repo, test_app):
    """
    Test retrieving orders by customer email.
    """
    with test_app.app_context():
        populate_test_data()

        # Create a sample order
        order = Orders(
            customeremail="customer1@example.com",
            totalprice=100.00,
            status="Preparing"
        )
        db.session.add(order)
        db.session.commit()

        orders = order_repo.get_orders_by_customer("customer1@example.com")
        assert len(orders) == 1
        assert orders[0]["status"] == "Preparing"

def test_update_order_status(order_repo, test_app):
    """
    Test updating the status of an order.
    """
    with test_app.app_context():
        populate_test_data()

        # Create a sample order
        order = Orders(
            customeremail="customer1@example.com",
            totalprice=100.00,
            status="Preparing"
        )
        db.session.add(order)
        db.session.commit()

        response = order_repo.update_order_status(order.orderid, "Out for Delivery")
        assert "message" in response
        assert "Out for Delivery" in response["message"]

        updated_order = Orders.query.get(order.orderid)
        assert updated_order.status == "Out for Delivery"

def test_close_order(order_repo, test_app):
    """
    Test closing an order (marking it as 'Done' and removing delivery assignment).
    """
    with test_app.app_context():
        populate_test_data()

        # Create a sample order and delivery assignment
        order = Orders(
            customeremail="customer1@example.com",
            totalprice=100.00,
            status="Out for Delivery"
        )
        db.session.add(order)
        db.session.commit()

        assignment = DeliveryAssignments(orderid=order.orderid, deliveryemail="delivery1@example.com")
        db.session.add(assignment)
        db.session.commit()

        response = order_repo.close_order(order.orderid)
        assert "message" in response
        assert "order closed successfully" in response["message"]

        closed_order = Orders.query.get(order.orderid)
        assert closed_order.status == "Done"

        deleted_assignment = DeliveryAssignments.query.filter_by(orderid=order.orderid).first()
        assert deleted_assignment is None
