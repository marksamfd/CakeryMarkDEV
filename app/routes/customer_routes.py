from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.customer_service import (get_all_products, get_product_details, get_cart_items, add_to_cart, remove_from_cart)
customer_routes = Blueprint('customer_routes', __name__)



''' ===================================== Product Endpoints ===================================== '''
# ------------------------------------------ all products for "Shop" page ------------------------------------------
@customer_routes.route('/customer/shop', methods=['GET'])
# @jwt_required()  
def shop():
    # a list of all products
    products = get_all_products()
    return jsonify(products), 200

# ------------------------------------------------ get the product details ------------------------------------------------
@customer_routes.route('/Product/<int:product_id>', methods=['GET'])
# @jwt_required()
def product_details(product_id):  # the data recived here from this endpoint will be a file with data came from the object of the product, we can slice it here for more specefic data for the final json reply for frontend
    # Fetch product details based on product_id
    product = get_product_details(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404
''' ------------------------------------------------------------------------------------------ '''

''' ===================================== Cart Endpoints ===================================== '''
# ---------------------------- Get cart items for a customer ----------------------------
@customer_routes.route('/Cart/<string:customeremail>', methods=['GET'])
def get_cart(customeremail):
    items = get_cart_items(customeremail)
    return jsonify(items), 200

# -------------------------------------- Add product to cart --------------------------------------
@customer_routes.route('/Cart/Add', methods=['POST'])
def add_cart_item():
    try: 
        data = request.get_json()
        customeremail = data.get("customeremail")
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
@customer_routes.route('/Cart/Remove', methods=['DELETE'])
def remove_cart_item():
    data = request.get_json()
    customeremail = data.get("customeremail")
    product_id = data.get("product_id")

    if not all([customeremail, product_id]):
        return jsonify({"error": "Invalid input"}), 400

    result = remove_from_cart(customeremail, product_id)
    return jsonify(result), 200