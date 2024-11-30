from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import jwt
from app.services.customer_service import (get_all_products, get_product_details, get_cart_items, add_to_cart, remove_from_cart,remove_from_cart,create_customized_cake,get_raw_materials,process_checkout,get_customer_orders)



customer_routes = Blueprint('customer_routes', __name__)


''' ===================================== Product Endpoints ===================================== '''
# ------------------------------------------ all products for "Shop" page ------------------------------------------
@customer_routes.route('/customer/shop', methods=['GET'])
@jwt_required()  
def shop():
    # a list of all products
    products = get_all_products()
    return jsonify(products), 200

# ------------------------------------------------ get the product details ------------------------------------------------
@customer_routes.route('/Product/<int:product_id>', methods=['GET'])
@jwt_required()
def product_details(product_id):  # the data recived here from this endpoint will be a file with data came from the object of the product, we can slice it here for more specefic data for the final json reply for frontend
    # Fetch product details based on product_id
    product = get_product_details(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404
''' ------------------------------------------------------------------------------------------ '''

''' ===================================== Cart Endpoints ===================================== '''
# ---------------------------- Get cart items for a customer ----------------------------
@customer_routes.route('/customer/Cart', methods=['GET'])
@jwt_required()
def get_cart():
    customer_email = get_jwt_identity()
    items = get_cart_items(customer_email)
    return jsonify(items), 200


# -------------------------------------- Add product to cart --------------------------------------
@customer_routes.route('/customer/Cart/Add', methods=['POST'])
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
@customer_routes.route('/customer/Cart/Remove', methods=['DELETE'])
@jwt_required()
def remove_cart_item():
    data = request.get_json()
    customeremail = get_jwt_identity()
    product_id = data.get("product_id")

    if not all([customeremail, product_id]):
        return jsonify({"error": "Invalid input"}), 400

    result = remove_from_cart(customeremail, product_id)
    return jsonify(result), 200

''' ===================================== Cake Customization ===================================== '''
# ------------------------- Send all the raw materials data -------------------------

@customer_routes.route("/App/User/Customer/Customize_Cake", methods=["GET"])
#@jwt_required()
def cust_cakes_prices():
    try:
        # Call the service function to retrieve data
        data = get_raw_materials()
        return jsonify({"data": data}), 200

    except Exception as e:
        # Return error response
        return jsonify({"error": str(e)}), 500


# ------------------------- Add the customized cake to the database  -------------------------
@customer_routes.route("/App/User/Customer/Customize_Cake/Create", methods=["POST"])
#@jwt_required()
def cust_cakes_create():
    try:
        # Extract email from JWT and JSON data
        #email = get_jwt_identity()
        data = request.get_json()
        email = data.get("email")
        # Call the service function to handle logic
        result = create_customized_cake(email, data)
        
        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500




'''=================================== Checkout Endpoint ==================================='''
@customer_routes.route('/customer/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        data = request.get_json() # data
        voucher_code = data.get("voucher")  
        customer_email = get_jwt_identity() 
        result = process_checkout(customer_email, voucher_code)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Error during checkout: {e}"}), 500

'''=================================== My Orders Endpoint ==================================='''
# ---------------------------- Get all orders for a customer ----------------------------
@customer_routes.route('/customer/orders', methods=['GET'])
@jwt_required()
def my_orders():
    customer_email = get_jwt_identity()

    try:
        orders = get_customer_orders(customer_email)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching orders: {e}"}), 500
