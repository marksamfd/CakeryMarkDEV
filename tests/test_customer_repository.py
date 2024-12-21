import pytest
from app.db import create_app, db
from app.Repositories.customer_repository import CustomerRepository
from app.models import Inventory, Cart, CartItems, CustomerUser, Review

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
def customer_repo():
    """
    Instantiates the CustomerRepository.
    """
    return CustomerRepository()


# Helper function to populate test data
def populate_test_data():
    """
    Populate the database with test data.
    """
    # Add products
    product1 = Inventory(productid=1, name="Chocolate Cake", price=25.00, category="Cake")
    product2 = Inventory(productid=2, name="Vanilla Cupcake", price=3.00, category="Cupcake")
    db.session.add_all([product1, product2])

    # Add customer
    customer = CustomerUser(
        customeremail="customer1@example.com",
        firstname="John",
        lastname="Doe",
        password="password123",
        phonenum="123456789",
    )
    db.session.add(customer)

    # Add cart
    cart = Cart(cartid=1, customeremail="customer1@example.com")
    db.session.add(cart)
    db.session.commit()


def test_get_all_products(customer_repo, test_app):
    """
    Test retrieving all products.
    """
    with test_app.app_context():
        populate_test_data()
        products = customer_repo.get_all_products()
        assert len(products) == 2
        assert products[0]["name"] == "Chocolate Cake"
        assert products[1]["name"] == "Vanilla Cupcake"


def test_add_item_to_cart_success(customer_repo, test_app):
    """
    Test successfully adding an item to the cart.
    """
    with test_app.app_context():
        populate_test_data()
        response = customer_repo.add_item_to_cart(
            customer_email="customer1@example.com", product_id=1, quantity=2
        )
        assert "message" in response
        assert response["message"] == "Added to cart successfully, cart id: 1"

        cart_items = CartItems.query.filter_by(cartid=1).all()
        assert len(cart_items) == 1
        assert cart_items[0].productid == 1
        assert cart_items[0].quantity == 2


def test_get_cart_success(customer_repo, test_app):
    """
    Test retrieving a customer's cart.
    """
    with test_app.app_context():
        populate_test_data()
        customer_repo.add_item_to_cart(
            customer_email="customer1@example.com", product_id=1, quantity=2
        )
        cart = customer_repo.get_cart("customer1@example.com")
        assert "cart_id" in cart
        assert cart["cart_id"] == 1
        assert len(cart["items"]) == 1
        assert cart["items"][0]["productid"] == 1
        assert cart["items"][0]["quantity"] == 2


def test_remove_item_from_cart(customer_repo, test_app):
    """
    Test removing an item from the cart.
    """
    with test_app.app_context():
        populate_test_data()
        customer_repo.add_item_to_cart(
            customer_email="customer1@example.com", product_id=1, quantity=2
        )
        response = customer_repo.remove_from_cart("customer1@example.com", product_id=1)
        assert "message" in response
        assert response["message"] == "Item removed from cart successfully"

        cart_items = CartItems.query.filter_by(cartid=1).all()
        assert len(cart_items) == 0


def test_place_review_success(customer_repo, test_app):
    """
    Test placing a product review.
    """
    with test_app.app_context():
        populate_test_data()
        response = customer_repo.place_review(
            customer_email="customer1@example.com", rating=5, product_id=1
        )
        assert "message" in response
        assert response["message"] == "User rating added successfully"

        review = Review.query.filter_by(
            customeremail="customer1@example.com", productid=1
        ).first()
        assert review is not None
        assert review.rating == 5


def test_place_review_invalid_product(customer_repo, test_app):
    """
    Test placing a review for an invalid product.
    """
    with test_app.app_context():
        populate_test_data()
        response = customer_repo.place_review(
            customer_email="customer1@example.com", rating=5, product_id=999
        )
        assert "message" in response
        assert response["message"] == "Product does not exist"


def test_increment_quantity(customer_repo, test_app):
    """
    Test incrementing the quantity of a cart item.
    """
    with test_app.app_context():
        populate_test_data()
        customer_repo.add_item_to_cart(
            customer_email="customer1@example.com", product_id=1, quantity=1
        )
        response = customer_repo.increment_quantity(
            customer_email="customer1@example.com", product_id=1, action="increment"
        )
        assert "message" in response
        assert response["message"] == "Quantity updated successfully"
        assert response["new_quantity"] == 2
