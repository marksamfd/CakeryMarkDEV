from app.db import create_app, db
from sqlalchemy.sql import text

# Create the app context for database access
app = create_app()

with app.app_context():
    try:
        # Test database connection
        print("Testing database connection...")
        db.session.execute(text("SELECT 1"))
        print("Database connection successful!")

        # Query 1: Fetch all customers
        print("\nFetching all customers...")
        query = text("SELECT CustomerEmail, FirstName, LastName, PhoneNum, AddressGoogleMapURL, CreatedAt FROM CustomerUser")
        results = db.session.execute(query).mappings().all()  # Use mappings() for dictionary-like results
        for row in results:
            print(dict(row))  # Safely convert each row to a dictionary

        # Query 2: Fetch customer by email
        customer_email = "anas.ahmad@example.com"
        print(f"\nFetching details for customer: {customer_email}")
        query = text("""
            SELECT CustomerEmail, FirstName, LastName, PhoneNum, AddressGoogleMapURL, CreatedAt
            FROM CustomerUser
            WHERE CustomerEmail = :customer_email
        """)
        result = db.session.execute(query, {"customer_email": customer_email}).mappings().first()  # Use mappings() for single result
        if result:
            print(dict(result))
        else:
            print("Customer not found.")

        # Query 3: Fetch all products in inventory
        print("\nFetching all products in inventory...")
        query = text("SELECT ProductID, Name, Description, Price, Category, CreatedAt FROM Inventory")
        results = db.session.execute(query).mappings().all()  # Use mappings()
        for row in results:
            print(dict(row))

        # Query 4: Fetch orders for a specific customer
        customer_email = "anas.ahmad@example.com"
        print(f"\nFetching orders for customer: {customer_email}")
        query = text("""
            SELECT OrderID, TotalPrice, Status, OrderDate, DeliveryDate
            FROM Orders
            WHERE CustomerEmail = :customer_email
        """)
        results = db.session.execute(query, {"customer_email": customer_email}).mappings().all()  # Use mappings()
        for row in results:
            print(dict(row))

        # Query 5: Fetch all items in a customer's cart
        print("\nFetching cart items for customer: anas.ahmad@example.com")
        query = text("""
            SELECT ci.CartItemID, i.Name, ci.Quantity, ci.Price
            FROM CartItems ci
            JOIN Cart c ON ci.CartID = c.CartID
            JOIN Inventory i ON ci.ProductID = i.ProductID
            WHERE c.CustomerEmail = :customer_email
        """)
        results = db.session.execute(query, {"customer_email": "anas.ahmad@example.com"}).mappings().all()  # Use mappings()
        for row in results:
            print(dict(row))

    except Exception as e:
        print("Error:", e)
