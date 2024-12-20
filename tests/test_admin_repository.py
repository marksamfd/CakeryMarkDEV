import pytest
from unittest.mock import patch
from app.db import create_app, db
from app.Repositories.admin_repository import AdminRepository
from app.Repositories.delivery_repository import DeliveryRepository
from app.models import (
    DeliveryUser,
    BakeryUser,
    CustomerUser,
    Voucher,
    Rawmaterials,
    Inventory,
    Orders,
    OrderItems,
)
from datetime import datetime, timezone, timedelta
from argon2 import PasswordHasher

# Initialize Password Hasher
ph = PasswordHasher()

# ===========================
# Fixtures
# ===========================

@pytest.fixture(scope='function')
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

@pytest.fixture(scope='function')
def client(test_app):
    """
    Provides a test client for the Flask application.
    """
    with test_app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def mock_delivery_repo():
    """
    Mocks the DeliveryRepository's find_available_delivery_user method.
    """
    with patch.object(DeliveryRepository, 'find_available_delivery_user', return_value="available_delivery@example.com") as mock:
        delivery_repo = DeliveryRepository()
        yield delivery_repo

@pytest.fixture(scope='function')
def admin_repo(mock_delivery_repo):
    """
    Instantiates the AdminRepository with the mocked DeliveryRepository.
    """
    return AdminRepository(delivery_repo=mock_delivery_repo)

# ===========================
# Helper Functions
# ===========================

def add_bakery_user(email, firstname="Bakery", lastname="User", phone="1234567890", password="password"):
    """
    Adds a BakeryUser to the database with hashed password.
    """
    bakery_user = BakeryUser(
        firstname=firstname,
        lastname=lastname,
        bakeryemail=email,
        phonenum=phone,
        password=ph.hash(password)
    )
    db.session.add(bakery_user)
    db.session.commit()
    return bakery_user

def add_delivery_user(email, firstname="Delivery", lastname="User", phone="0987654321", password="password"):
    """
    Adds a DeliveryUser to the database with hashed password.
    """
    delivery_user = DeliveryUser(
        firstname=firstname,
        lastname=lastname,
        phonenum=phone,
        deliveryemail=email,
        password=ph.hash(password)
    )
    db.session.add(delivery_user)
    db.session.commit()
    return delivery_user

def add_customer_user(email, firstname="Customer", lastname="User", phone="1122334455", password="password"):
    """
    Adds a CustomerUser to the database with hashed password.
    """
    customer_user = CustomerUser(
        firstname=firstname,
        lastname=lastname,
        customeremail=email,
        phonenum=phone,
        password=ph.hash(password),
        addressgooglemapurl="http://maps.example.com",
        createdat=datetime.now(timezone.utc)
    )
    db.session.add(customer_user)
    db.session.commit()
    return customer_user

def add_voucher(vouchercode, discountpercentage):
    """
    Adds a Voucher to the database.
    """
    voucher = Voucher(
        vouchercode=vouchercode,
        discountpercentage=discountpercentage
    )
    db.session.add(voucher)
    db.session.commit()
    return voucher

def add_order(orderdate, totalprice, deliveryemail=None):
    """
    Adds an Order to the database.
    """
    order = Orders(
        orderdate=orderdate,
        totalprice=totalprice,
        deliveryemail=deliveryemail
    )
    db.session.add(order)
    db.session.commit()
    return order

def add_order_item(orderid, productid, quantity, priceatorder):
    """
    Adds an OrderItem to the database.
    Ensures that the referenced product exists in Inventory.
    """
    # Ensure the product exists in Inventory
    product = Inventory.query.filter_by(productid=productid).first()
    if not product:
        # Create a default product if it doesn't exist
        product = Inventory(name=f"Product {productid}", productid=productid, price=priceatorder)
        db.session.add(product)
        db.session.commit()

    order_item = OrderItems(
        orderid=orderid,
        productid=productid,
        customcakeid=None,  # Adjust as needed
        quantity=quantity,
        priceatorder=priceatorder
    )
    db.session.add(order_item)
    db.session.commit()
    return order_item

def add_raw_material(item, price, category):
    """
    Adds a Rawmaterial to the database with the specified category.
    """
    raw_material = Rawmaterials(
        item=item,
        price=price,
        category=category
    )
    db.session.add(raw_material)
    db.session.commit()
    return raw_material

# ===========================
# Test Cases
# ===========================

# ---------------------------
# Staff User Management Tests
# ---------------------------

def test_get_staff_users(admin_repo, test_app):
    """
    Tests retrieval of all staff users.
    """
    with test_app.app_context():
        # Add sample delivery and bakery users
        add_delivery_user("delivery1@example.com")
        add_delivery_user("delivery2@example.com")
        add_bakery_user("bakery1@example.com")
        add_bakery_user("bakery2@example.com")
        
        staff = admin_repo.get_staff_users()
        
        assert len(staff) == 4
        assert "delivery1@example.com" in staff
        assert "delivery2@example.com" in staff
        assert "bakery1@example.com" in staff
        assert "bakery2@example.com" in staff
        assert staff["delivery1@example.com"]["role"] == "delivery"
        assert staff["bakery1@example.com"]["role"] == "baker"

def test_add_bakery_user_success(admin_repo, test_app):
    """
    Tests successful addition of a bakery user.
    """
    with test_app.app_context():
        response = admin_repo.add_bakery_user(
            firstname="New",
            lastname="Baker",
            email="new_baker@example.com",
            phone="5555555555",
            password="securepassword"
        )
        
        assert "message" in response
        assert response["message"] == "baker user new_baker@example.com was added"
        
        # Verify in database
        baker = BakeryUser.query.filter_by(bakeryemail="new_baker@example.com").first()
        assert baker is not None
        assert baker.firstname == "New"
        assert baker.lastname == "Baker"

def test_add_bakery_user_existing_email(admin_repo, test_app):
    """
    Tests adding a bakery user with an existing email, expecting an error.
    """
    with test_app.app_context():
        # First addition
        admin_repo.add_bakery_user(
            firstname="Existing",
            lastname="Baker",
            email="existing_baker@example.com",
            phone="6666666666",
            password="password123"
        )
        
        # Second addition with the same email
        response = admin_repo.add_bakery_user(
            firstname="Existing",
            lastname="Baker",
            email="existing_baker@example.com",
            phone="6666666666",
            password="password123"
        )
        
        assert "error" in response
        assert "error adding baker user" in response["error"]

def test_delete_baker_user_success(admin_repo, test_app):
    """
    Tests successful deletion of a bakery user.
    """
    with test_app.app_context():
        # Add a baker to delete
        add_bakery_user("delete_baker@example.com")
        
        response = admin_repo.delete_baker_user("delete_baker@example.com")
        
        assert "message" in response
        assert response["message"] == "baker deleted successfully"
        
        # Verify deletion
        baker = BakeryUser.query.filter_by(bakeryemail="delete_baker@example.com").first()
        assert baker is None

def test_delete_baker_user_not_found(admin_repo, test_app):
    """
    Tests deletion of a non-existent bakery user, expecting an error.
    """
    with test_app.app_context():
        response = admin_repo.delete_baker_user("nonexistent_baker@example.com")
        
        assert "error" in response
        assert "user not found" in response["error"]

def test_add_delivery_user_success(admin_repo, test_app):
    """
    Tests successful addition of a delivery user.
    """
    with test_app.app_context():
        response = admin_repo.add_delivery_user(
            firstname="New",
            lastname="Delivery",
            email="new_delivery@example.com",
            phone="7777777777",
            password="securepassword"
        )
        
        assert "message" in response
        assert response["message"] == "delivery user new_delivery@example.com was added"
        
        # Verify in database
        delivery_user = DeliveryUser.query.filter_by(deliveryemail="new_delivery@example.com").first()
        assert delivery_user is not None
        assert delivery_user.firstname == "New"
        assert delivery_user.lastname == "Delivery"

def test_delete_delivery_user_success(admin_repo, test_app):
    """
    Tests successful deletion of a delivery user with order reassignment.
    """
    with test_app.app_context():
        # Add a delivery user to delete
        add_delivery_user("delivery_to_delete@example.com")
        
        # Add an available delivery user for reassignment
        add_delivery_user("available_delivery@example.com")
        
        # Add an order assigned to the delivery user to be deleted
        order = add_order(
            orderdate=datetime.now(timezone.utc),
            totalprice=100.0,
            deliveryemail="delivery_to_delete@example.com"
        )
        
        # Call delete_delivery_user
        response = admin_repo.delete_delivery_user("delivery_to_delete@example.com")
        
        assert "message" in response
        assert response["message"] == "Delivery user deleted successfully and orders reassigned."
        
        # Verify deletion
        delivery_user = DeliveryUser.query.filter_by(deliveryemail="delivery_to_delete@example.com").first()
        assert delivery_user is None
        
        # Verify order reassignment
        reassigned_order = Orders.query.filter_by(orderid=order.orderid).first()
        assert reassigned_order.deliveryemail == "available_delivery@example.com"

def test_delete_delivery_user_no_available_reassignment(admin_repo, test_app):
    """
    Tests deletion of a delivery user when no delivery users are available for order reassignment.
    Expects an error.
    """
    with test_app.app_context():
        # Mock the find_available_delivery_user to return None
        with patch.object(DeliveryRepository, 'find_available_delivery_user', return_value=None):
            # Add a delivery user to delete
            add_delivery_user("delivery_no_reassign@example.com")
            
            # Add an order assigned to the delivery user to be deleted
            add_order(
                orderdate=datetime.now(timezone.utc),
                totalprice=150.0,
                deliveryemail="delivery_no_reassign@example.com"
            )
            
            # Attempt to delete the delivery user
            response = admin_repo.delete_delivery_user("delivery_no_reassign@example.com")
            
            assert "error" in response
            assert response["error"] == "No available delivery users to reassign orders."

# ---------------------------
# Customer Management Tests
# ---------------------------

def test_get_customers(admin_repo, test_app):
    """
    Tests retrieval of all customers.
    """
    with test_app.app_context():
        # Add sample customers
        add_customer_user("customer1@gmail.com", firstname="John", lastname="Doe")
        add_customer_user("customer2@gmail.com", firstname="Jane", lastname="Smith")
        
        customers = admin_repo.get_customers()
        
        assert len(customers) == 2
        assert {
            "name": "John Doe",
            "email": "customer1@gmail.com",
            "phone": "1122334455"
        } in customers
        assert {
            "name": "Jane Smith",
            "email": "customer2@gmail.com",
            "phone": "1122334455"
        } in customers

# ---------------------------
# Voucher Management Tests
# ---------------------------

def test_get_vouchers(admin_repo, test_app):
    """
    Tests retrieval of all vouchers.
    """
    with test_app.app_context():
        # Add sample vouchers
        add_voucher("DISCOUNT10", 10)
        add_voucher("DISCOUNT20", 20)
        
        vouchers = admin_repo.get_vouchers()
        
        assert len(vouchers) == 2
        assert "DISCOUNT10" in vouchers
        assert vouchers["DISCOUNT10"]["discount_percentage"] == 10
        assert "DISCOUNT20" in vouchers
        assert vouchers["DISCOUNT20"]["discount_percentage"] == 20

def test_add_voucher_success(admin_repo, test_app):
    """
    Tests successful addition of a voucher.
    """
    with test_app.app_context():
        response, status_code = admin_repo.add_voucher("DISCOUNT30", 30)
        
        assert status_code == 200
        assert response["message"] == "Voucher added successfully"
        
        # Verify in database
        voucher = Voucher.query.filter_by(vouchercode="DISCOUNT30").first()
        assert voucher is not None
        assert voucher.discountpercentage == 30

def test_edit_voucher_success(admin_repo, test_app):
    """
    Tests successful editing of a voucher.
    """
    with test_app.app_context():
        # Add a voucher to edit
        add_voucher("EDITVOUCHER", 15)
        
        response, status_code = admin_repo.edit_voucher("EDITVOUCHER", 25)
        
        assert status_code == 200
        assert response["message"] == "Voucher updated successfully"
        
        # Verify in database
        voucher = Voucher.query.filter_by(vouchercode="EDITVOUCHER").first()
        assert voucher.discountpercentage == 25

def test_edit_voucher_not_found(admin_repo, test_app):
    """
    Tests editing a non-existent voucher, expecting an error.
    """
    with test_app.app_context():
        response, status_code = admin_repo.edit_voucher("NONEXISTENT", 50)
        
        assert status_code == 404
        assert response["error"] == "Voucher not found"

def test_delete_voucher_success(admin_repo, test_app):
    """
    Tests successful deletion of a voucher.
    """
    with test_app.app_context():
        # Add a voucher to delete
        add_voucher("DELETEVOUCHER", 20)
        
        response, status_code = admin_repo.delete_voucher("DELETEVOUCHER")
        
        assert status_code == 200
        assert response["message"] == "Voucher deleted successfully"
        
        # Verify deletion
        voucher = Voucher.query.filter_by(vouchercode="DELETEVOUCHER").first()
        assert voucher is None

def test_delete_voucher_not_found(admin_repo, test_app):
    """
    Tests deletion of a non-existent voucher, expecting an error.
    """
    with test_app.app_context():
        response, status_code = admin_repo.delete_voucher("NONEXISTENT")
        
        assert status_code == 404
        assert response["error"] == "Voucher not found"

# ---------------------------
# Raw Materials and Products Management Tests
# ---------------------------

def test_products_rawMats(admin_repo, test_app):
    """
    Tests retrieval of all products and raw materials.
    """
    with test_app.app_context():
        # Add sample products and raw materials with category
        product1 = Inventory(name="Cake", productid=1, price=20.0)
        product2 = Inventory(name="Bread", productid=2, price=5.0)
        raw1 = add_raw_material(item="Flour", price=2.0, category="Baking")
        raw2 = add_raw_material(item="Sugar", price=1.5, category="Baking")
        
        db.session.add_all([product1, product2])
        db.session.commit()
        
        items = admin_repo.prducts_rawMats()
        
        assert len(items) == 4
        assert "Cake" in items
        assert items["Cake"]["price"] == 20.0
        assert "Bread" in items
        assert items["Bread"]["price"] == 5.0
        assert "Flour" in items
        assert items["Flour"]["price"] == 2.0
        assert "Sugar" in items
        assert items["Sugar"]["price"] == 1.5

def test_edit_product_price_success(admin_repo, test_app):
    """
    Tests successful editing of a product's price.
    """
    with test_app.app_context():
        # Add a product to edit
        product = Inventory(name="Cookie", productid=3, price=3.0)
        db.session.add(product)
        db.session.commit()
        
        response = admin_repo.edit_product(price=4.5, product_id=3)
        
        assert "message" in response
        assert response["message"] == "Product price updated successfully"
        
        # Verify in database
        updated_product = Inventory.query.filter_by(productid=3).first()
        assert updated_product.price == 4.5

def test_edit_raw_material_price_success(admin_repo, test_app):
    """
    Tests successful editing of a raw material's price.
    """
    with test_app.app_context():
        # Add a raw material to edit with category
        raw = add_raw_material(item="Eggs", price=0.5, category="Dairy")
        
        response = admin_repo.edit_product(price=0.75, rawItem="Eggs")
        
        assert "message" in response
        assert response["message"] == "Raw material price updated successfully"
        
        # Verify in database
        updated_raw = Rawmaterials.query.filter_by(item="Eggs").first()
        assert updated_raw.price == 0.75

def test_edit_product_invalid(admin_repo, test_app):
    """
    Tests editing a product without providing product_id or rawItem, expecting an error.
    """
    with test_app.app_context():
        response = admin_repo.edit_product(price=10.0)
        
        assert "error" in response
        assert response["error"] == "product_id or rawItem must be provided"

# ---------------------------
# Dashboard Data Tests
# ---------------------------

def test_get_dashboard_data(admin_repo, test_app):
    """
    Tests retrieval of dashboard data with sample orders and order items.
    """
    with test_app.app_context():
        # Add sample products to Inventory
        product1 = Inventory(name="Cake", productid=1, price=20.0)
        product2 = Inventory(name="Bread", productid=2, price=5.0)
        db.session.add_all([product1, product2])
        db.session.commit()

        # Add sample orders and order items
        # Order within last 5 days
        order1 = add_order(
            orderdate=datetime.now(timezone.utc) - timedelta(days=2),
            totalprice=50.0,
            deliveryemail="delivery1@example.com"
        )
        add_order_item(orderid=order1.orderid, productid=1, quantity=2, priceatorder=20.0)

        # Order within last 5 days
        order2 = add_order(
            orderdate=datetime.now(timezone.utc) - timedelta(days=1),
            totalprice=30.0,
            deliveryemail="delivery2@example.com"
        )
        add_order_item(orderid=order2.orderid, productid=2, quantity=3, priceatorder=5.0)

        # Order older than 5 days
        order3 = add_order(
            orderdate=datetime.now(timezone.utc) - timedelta(days=10),
            totalprice=100.0,
            deliveryemail="delivery1@example.com"
        )
        add_order_item(orderid=order3.orderid, productid=1, quantity=5, priceatorder=20.0)

        dashboard = admin_repo.get_dashboard_data()

        assert dashboard["status"] == "success"
        data = dashboard["data"]

        # Check total_price_by_date
        assert len(data["total_price_by_date"]) == 2
        assert {
            "Date": (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%d/%m/%Y"),
            "Total Price": 50.0
        } in data["total_price_by_date"]
        assert {
            "Date": (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%d/%m/%Y"),
            "Total Price": 30.0
        } in data["total_price_by_date"]

        # Check best_sold_items
        assert len(data["best_sold_items"]) == 2
        # ProductID 1: quantity=2, total_price=40.0
        # ProductID 2: quantity=3, total_price=15.0
        assert {
            "itemName": "Cake",
            "price": 40.0,
            "qty": 2
        } in data["best_sold_items"]
        assert {
            "itemName": "Bread",
            "price": 15.0,
            "qty": 3
        } in data["best_sold_items"]

def test_get_dashboard_data_no_orders(admin_repo, test_app):
    """
    Tests retrieval of dashboard data when there are no orders.
    Expects empty data structures.
    """
    with test_app.app_context():
        dashboard = admin_repo.get_dashboard_data()

        assert dashboard["status"] == "success"
        data = dashboard["data"]

        assert len(data["total_price_by_date"]) == 0
        assert len(data["best_sold_items"]) == 0

# ===========================
# Additional Notes
# ===========================

"""
1. **Ensure Models Are Correctly Defined:**
   - The `Rawmaterials` model must have `category` set as `nullable=False` to enforce the NOT NULL constraint.
   - Foreign key relationships in models like `OrderItems` should correctly reference existing entries in `Inventory` and `Orders`.

2. **Password Hashing Consistency:**
   - The helper functions hash passwords using `argon2`. Ensure that your actual repository methods handle password verification accordingly.

3. **Use Factory Libraries (Optional):**
   - For larger projects, consider using libraries like `factory_boy` to manage test data creation more efficiently.

4. **Database Schema Consistency:**
   - Ensure that your database schema matches the models, especially regarding constraints and relationships.

5. **Running the Tests:**
   - Execute the tests using the following command from your project's root directory:
     ```bash
     python -m pytest tests/test_admin_repository.py
     ```
"""

