# from app.db import create_app, db
# from app.models import Cart, Inventory, CartItems
# from app.services.customer_service import add_to_cart

# def test_add_to_cart():
#     # Create the Flask application
#     app = create_app()
#     with app.app_context():
#         # Ensure the database is connected
#         # db.session.execute("SELECT 1")
#         # print("Database connected successfully!")

#         # Test data
#         customeremail = "anas.ahmad@gmail.com"
#         product_id = 1  # Make sure this product ID exists in the Inventory table
#         quantity = 2

#         # Test: Add to cart
#         result = add_to_cart(customeremail, product_id, quantity)
#         print("Result of add_to_cart:", result)

#         # Verify the result in the database
#         cart_items = CartItems.query.all()
#         for item in cart_items:
#             print({
#                 "cartitemid": item.cartitemid,
#                 "cartid": item.cartid,
#                 "productid": item.productid,
#                 "quantity": item.quantity,
#                 "price": str(item.price)
#             })

# if __name__ == "__main__":
#     test_add_to_cart()
