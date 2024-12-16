from flask import Blueprint, request, jsonify
from app.Services.customer_service import CustomerService
from flask_jwt_extended import jwt_required, get_jwt_identity

customer_controller = Blueprint("customer_controller", __name__)
customer_service = CustomerService()

'''=================================== Shop ===================================='''  # - checked
@customer_controller.route("/cakery/user/customer/Shop",methods=["GET"]) # (Shop Page) 
def list_products():
    """
    List all available products 
    """
    products = customer_service.list_products()
    return jsonify(products), 200
# ----------------------------------------------------------------------------------

'''=================================== Product Detail ===================================='''  # - checked
@customer_controller.route("/cakery/user/customer/Product/<int:product_id>",methods=["GET"]) # (Product Detail Page) 
def get_product_details(product_id):
    """
    get the details of a specific product
    """
    product = customer_service.view_product_details(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404
# ----------------------------------------------------------------------------------

'''=================================== Cart  ====================================''' # - checked
@customer_controller.route("/cakery/user/customer/Cart/<customer_email>", methods=["GET"]) # (Cart Page) 
def get_cart(customer_email):
    """
    get the customer's cart
    """
    cart = customer_service.view_cart(customer_email)
    return jsonify(cart), 200
# ----------------------------------------------------------------------------------


'''=================================== Add to Cart ===================================='''  # - checked, but the files have to be run speratley from repos -> services -> controllers, check the database after restrting the app
@customer_controller.route("/cakery/user/customer/Cart/Add/<customer_email>", methods=["POST"]) # (Cart Page)
# @jwt_required()
def add_to_cart(customer_email):
    """
    add a product to the customer's cart
    """
    try:
        # customer_email = get_jwt_identity()
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        custom_cake_id = data.get("custom_cake_id")
        response = customer_service.add_to_cart(customer_email,product_id,quantity,custom_cake_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f" (route) can't add a product to the cart: {e}"}), 400
# ----------------------------------------------------------------------------------


'''=================================== Remove from Cart ===================================='''  # - checked
@customer_controller.route("/cakery/user/customer/Cart/Remove/<customer_email>",methods=["DELETE"]) # (Cart Page)
def remove_from_cart(customer_email):
    """
    Remove a product from the customer's cart
    """
    try:
        data = request.get_json()
        # customer_email =  #
        product_id = data.get("product_id")

        response = customer_service.remove_from_cart(customer_email, product_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"(route) error in removing product from cart: {e}"}), 400
# ----------------------------------------------------------------------------------


'''=================================== Customize Cake ===================================='''
@customer_controller.route("/cakery/user/customer/Customize_Cake", methods=["GET"])
def view_raw_materials():
     """
     View raw materials available for cake customization
     """
     raw_materials = customer_service.view_raw_materials()
     return jsonify(raw_materials), 200
# # ----------------------------------------------------------------------------------

# '''=================================== Create Custom Cake ===================================='''
@customer_controller.route("/cakery/user/customer/Customize_Cake/Create/<customer_email>", methods=["POST"]) # (Customize Cake Page)
def create_custom_cake(customer_email):
     """
     Create a customized cake and add it to the cart.
     """
     try:
         data = request.get_json()
         #customer_email = request.headers.get("customer_email")  # testing
         response = customer_service.create_custom_cake(customer_email, data)
         return jsonify(response), 200
     except Exception as e:
         return jsonify({"error": f"Error creating custom cake: {e}"}), 400
# ----------------------------------------------------------------------------------

'''=================================== Checkout ===================================='''  # - issue (voucher code)
@customer_controller.route("/cakery/user/customer/Checkout/<customer_email>", methods=["POST"])
def checkout(customer_email):
    """
    Checkout the customer's cart.
    """
    try:
        data = request.get_json()
        # customer_email =  
        voucher_code = data.get("voucher")
        response = customer_service.checkout(customer_email, voucher_code)
        if "error" in response:
            return jsonify(response), 400
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"(route) error during checkout: {e}"}), 500
# ----------------------------------------------------------------------------------


'''=================================== View Orders ===================================='''  # - checked
@customer_controller.route("/cakery/user/customer/Orders/<customer_email>", methods=["GET"]) # (Customer orders Page)
def view_orders(customer_email):
    """
    View all orders of the customer
    """
    # customer_email =   # testing
    orders = customer_service.view_customer_orders(customer_email)
    return jsonify(orders), 200
# ----------------------------------------------------------------------------------

'''=================================== Edit customer data ====================================''' 
@customer_controller.route("/cakery/user/customer/EditData/<customer_email>", methods=["PUT"]) 
def edit_customer_data(customer_email):
    
    data = request.get_json()
    response, status_code = customer_service.update_data(customer_email,data)
    return jsonify(response), status_code
# ----------------------------------------------------------------------------------
