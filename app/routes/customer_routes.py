from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from app.routes.checkout_routes import checkout
from app.services.checkout_service import process_checkout
from app.services.customer_service import (
    get_all_products,
    get_product_details,
    get_cart_items,
    add_to_cart,
    remove_from_cart,
)
from app.routes.order_routes import my_orders

customer_routes = Blueprint("customer_routes", __name__)


""" ===================================== Product Endpoints ===================================== """


# ------------------------------------------ all products for "Shop" page ------------------------------------------
@customer_routes.route("/customer/shop", methods=["GET"])
@jwt_required()
def shop():
    # a list of all products
    products = get_all_products()
    return jsonify(products), 200


# ------------------------------------------------ get the product details ------------------------------------------------
@customer_routes.route("/Product/<int:product_id>", methods=["GET"])
@jwt_required()
def product_details(
    product_id,
):  # the data recived here from this endpoint will be a file with data came from the object of the product, we can slice it here for more specefic data for the final json reply for frontend
    # Fetch product details based on product_id
    product = get_product_details(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


""" ------------------------------------------------------------------------------------------ """

""" ===================================== Cart Endpoints ===================================== """


# ---------------------------- Get cart items for a customer ----------------------------
@customer_routes.route("/customer/Cart", methods=["GET"])
@jwt_required()
def get_cart():
    customer_email = get_jwt_identity()
    items = get_cart_items(customer_email)
    return jsonify(items), 200


# -------------------------------------- Add product to cart --------------------------------------
@customer_routes.route("/customer/Cart/Add", methods=["POST"])
@jwt_required()
def add_cart_item():
    try:
        data = request.get_json()
        customeremail = get_jwt_identity()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        print("customeremail:", customeremail)
        print("----test----")
    except Exception as e:
        print("Error in add_cart_item")
        print(f"Error: {e}")
        return jsonify({"error": "Invalid input"}), 400
    # if not all([customeremail, product_id, quantity]):
    #     return jsonify({"error": "Invalid input ya anas"}), 400

    result = add_to_cart(customeremail, product_id, quantity)
    return jsonify(result), 200


# ------------------------- Remove product from cart -------------------------
@customer_routes.route("/customer/Cart/Remove", methods=["DELETE"])
@jwt_required()
def remove_cart_item():
    data = request.get_json()
    customeremail = get_jwt_identity()
    product_id = data.get("product_id")

    if not all([customeremail, product_id]):
        return jsonify({"error": "Invalid input"}), 400

    result = remove_from_cart(customeremail, product_id)
    return jsonify(result), 200


""" ===================================== Checkout Endpoints ===================================== """


# ---------------------------- Process Checkout ----------------------------
@customer_routes.route("/customer/checkout", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        customeremail = data.get("customeremail")

        # Delegate checkout processing to the service layer
        result = process_checkout(customeremail, data)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 201
    except Exception as e:
        print(f"Error in /customer/checkout: {e}")
        return jsonify({"error": "Internal server error"}), 500


""" ================================ Order Endpoints ================================= """
""" ===================================== Order Endpoints ===================================== """


# ---------------------------- Get Orders ----------------------------
@customer_routes.route("/customer/orders", methods=["GET"])
def orders():
    return my_orders()
