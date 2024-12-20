import pytest
from app.db import create_app, db
from app.Repositories.baker_repository import BakerRepository
from app.models import Orders, OrderItems, Inventory, CustomerUser, CustomizeCake

@pytest.fixture(scope="function")
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def baker_repo():
    return BakerRepository()

# Helper function to add test data
def populate_test_data():
    # Add customers
    customer1 = CustomerUser(
        customeremail="tasneem.mohamed@gmail.com",
        firstname="Tasneem",
        lastname="Mohamed",
        password="passTasneem",
        phonenum="112233445"
    )
    customer2 = CustomerUser(
        customeremail="anas.ahmad@gmail.com",
        firstname="Anas",
        lastname="Ahmad",
        password="passAnas",
        phonenum="123456789"
    )
    db.session.add_all([customer1, customer2])
    db.session.commit()

    # Add orders
    order1 = Orders(orderid=1, customeremail="anas.ahmad@gmail.com", totalprice=72.00, status="Pending")
    order3 = Orders(orderid=3, customeremail="tasneem.mohamed@gmail.com", totalprice=25.00, status="Out for Delivery")
    db.session.add_all([order1, order3])
    db.session.commit()

    # Add inventory
    product1 = Inventory(productid=1, name="Chocolate Cake", price=25.00, category="Cake")
    product2 = Inventory(productid=2, name="Vanilla Cupcake", price=3.00, category="Cupcake")
    db.session.add_all([product1, product2])
    db.session.commit()

    # Add custom cakes
    custom_cake = CustomizeCake(
        customizecakeid=1,
        numlayers=2,
        cakeshape="Round",
        cakesize="Medium",
        cakeflavor="Chocolate",
        message="Happy Birthday!"
    )
    db.session.add(custom_cake)
    db.session.commit()

    # Add order items
    item1 = OrderItems(orderid=1, productid=2, quantity=4, priceatorder=3.0)  # Vanilla Cupcakes
    item2 = OrderItems(orderid=1, customcakeid=1, quantity=1, priceatorder=60.0)  # Custom Cake
    item3 = OrderItems(orderid=3, productid=1, quantity=1, priceatorder=25.0)  # Chocolate Cake
    db.session.add_all([item1, item2, item3])
    db.session.commit()

def test_get_all_orders(baker_repo, test_app):
    with test_app.app_context():
        populate_test_data()
        orders = baker_repo.get_all_orders()
        assert len(orders) == 2
        assert orders[0]["orderID"] == 1
        assert orders[1]["orderID"] == 3

def test_get_order_details(baker_repo, test_app):
    with test_app.app_context():
        populate_test_data()
        order_details = baker_repo.get_order_details(1)
        assert order_details["orderID"] == 1
        assert len(order_details["items"]) == 2  # One product and one custom cake
        assert len(order_details["customCake"]) == 1  # Custom Cake
        assert order_details["customCake"][0]["customizecakeid"] == 1  # Correct field reference
        assert order_details["customCake"][0]["cakeshape"] == "Round"  # Validate other fields

def test_update_order_status(baker_repo, test_app):
    with test_app.app_context():
        populate_test_data()
        response = baker_repo.update_order_status(1, "Prepared")
        assert response["message"] == " Order status updated to Prepared"
        updated_order = Orders.query.get(1)
        assert updated_order.status == "Prepared"