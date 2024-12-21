from flask import Blueprint, request, jsonify
from app.Services.customer_service import CustomerService
from app.Services.otp_service import OTPService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.Middlewares.auth_middleware import token_required

customer_controller = Blueprint("customer_controller", __name__)
customer_service = CustomerService()

"""=================================== Shop ===================================="""  # - checked


@customer_controller.route("/cakery/user/customer/Shop", methods=["GET"])  # (Shop Page)
def list_products():
    """
    List All Available Products
    ---
    tags:
      - Customer
    summary: Retrieve a list of all available products in the shop
    produces:
      - application/json
    responses:
      200:
        description: A list of available products
        schema:
          type: array
          items:
            type: object
            properties:
              product_id:
                type: integer
                example: 501
              name:
                type: string
                example: "Chocolate Cake"
              description:
                type: string
                example: "Delicious chocolate layered cake"
              price:
                type: number
                format: float
                example: 25.50
              available_stock:
                type: integer
                example: 100
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while fetching products."
            error:
              type: string
              example: "Detailed error message."
    """
    try:
        products = customer_service.list_products()
        return jsonify(products), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while fetching products.",
                    "error": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""=================================== Product Detail ===================================="""  # - checked


@customer_controller.route(
    "/cakery/user/customer/Product/<int:product_id>", methods=["GET"]
)  # (Product Detail Page)
# @token_required(roles=["customer"])
def get_product_details(product_id):
    """
    Get Specific Product Details
    ---
    tags:
      - Customer
    summary: Retrieve detailed information about a specific product by its ID
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: The ID of the product to retrieve details for
        example: 501
    produces:
      - application/json
    responses:
      200:
        description: Detailed information of the specified product
        schema:
          type: object
          properties:
            product_id:
              type: integer
              example: 501
            name:
              type: string
              example: "Chocolate Cake"
            description:
              type: string
              example: "Delicious chocolate layered cake"
            price:
              type: number
              format: float
              example: 25.50
            available_stock:
              type: integer
              example: 100
            ingredients:
              type: array
              items:
                type: string
              example: ["Flour", "Sugar", "Cocoa Powder", "Eggs", "Butter"]
      404:
        description: Product not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Product not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while fetching product details."
            error:
              type: string
              example: "Detailed error message."
    """
    try:
        product = customer_service.view_product_details(product_id)
        if product:
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while fetching product details.",
                    "error": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""=================================== Cart ===================================="""  # - checked


@customer_controller.route("/cakery/user/customer/Cart", methods=["GET"])  # (Cart Page)
@token_required(roles=["customer"])
def get_cart():
    """
    Get Customer's Cart
    ---
    tags:
      - Customer
    summary: Retrieve the contents of the authenticated customer's cart
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: The authenticated customer's cart details
        schema:
          type: object
          properties:
            cart_id:
              type: integer
              example: 301
            items:
              type: array
              items:
                type: object
                properties:
                  product_id:
                    type: integer
                    example: 501
                  custom_cake_id:
                    type: integer
                    example: 1001
                  quantity:
                    type: integer
                    example: 2
                  price:
                    type: number
                    format: float
                    example: 25.50
                  product_name:
                    type: string
                    example: "Chocolate Cake"
      404:
        description: Cart not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Cart not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while fetching the cart."
            error:
              type: string
              example: "Detailed error message."
    """
    try:
        customer_email = request.user
        cart = customer_service.view_cart(customer_email)
        return jsonify(cart), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while fetching the cart.",
                    "error": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""=================================== Add to Cart ===================================="""  # - checked


@customer_controller.route(
    "/cakery/user/customer/Cart/Add", methods=["POST"]
)  # (Cart Page)
@token_required(roles=["customer"])
def add_to_cart():
    """
    Add Product to Cart
    ---
    tags:
      - Customer
    summary: Add a product or a customized cake to the authenticated customer's cart
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details of the product to add to the cart
        required: true
        schema:
          type: object
          required:
            - product_id
            - quantity
          properties:
            product_id:
              type: integer
              example: 501
            quantity:
              type: integer
              example: 2
            custom_cake_id:
              type: integer
              example: 1001
    responses:
      200:
        description: Product added to cart successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Added to cart successfully, cart id: 301"
      400:
        description: Bad Request - Missing product ID, quantity, or other validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Order ID and status are required"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while adding the product to the cart."
            error:
              type: string
              example: "Detailed error message."
    """
    try:
        customer_email = request.user
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity")
        custom_cake_id = data.get("custom_cake_id")
        response = customer_service.add_to_cart(
            customer_email, product_id, quantity, custom_cake_id
        )
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f" (route) can't add a product to the cart: {e}"}), 400


# *****************************************************************************************************
# ------------------------------------ increment/decrement quantity ------
# *****************************************************************************************************
@customer_controller.route(
    "/cakery/user/customer/Cart/Increment", methods=["PUT"]
)  # (Cart Page)
@token_required(roles=["customer"])
def increment_quantity():
    """
    Update Cart Item Quantity
    ---
    tags:
      - Customer
    summary: Increment or decrement the quantity of a specific product in the authenticated customer's cart
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details for updating product quantity
        required: true
        schema:
          type: object
          required:
            - product_id
            - action
          properties:
            product_id:
              type: integer
              example: 1
            action:
              type: string
              enum: ["decrement", "increment"]
              example: "increment"
    responses:
      200:
        description: Quantity updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Product quantity updated successfully."
            new_quantity:
              type: integer
              example: 3
      400:
        description: Bad Request - Missing product ID, invalid action, or other validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid action provided. Must be 'increment' or 'decrement'."
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while updating product quantity."
    """
    customer_email = request.user
    data = request.get_json()
    response = customer_service.incrementQuantity(data, customer_email)
    return jsonify(response), 200


"""=================================== Remove from Cart ===================================="""  # - checked


@customer_controller.route(
    "/cakery/user/customer/Cart/Remove", methods=["DELETE"]
)  # (Cart Page)
@token_required(roles=["customer"])
def remove_from_cart():
    """
    Remove Product from Cart
    ---
    tags:
      - Customer
    summary: Remove a specific product from the authenticated customer's cart
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details of the product to remove from the cart
        required: true
        schema:
          type: object
          required:
            - product_id
          properties:
            product_id:
              type: integer
              example: 501
    responses:
      200:
        description: Product removed from cart successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Item removed from cart successfully"
      400:
        description: Bad Request - Missing product ID or other validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing product ID"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while removing the item from the cart."
    """
    try:
        data = request.get_json()
        customer_email = request.user
        product_id = data.get("product_id")

        response = customer_service.remove_from_cart(customer_email, product_id)
        return jsonify(response), 200
    except Exception as e:
        return (
            jsonify({"error": f"(route) error in removing product from cart: {e}"}),
            400,
        )


# ----------------------------------------------------------------------------------

"""=================================== Customize Cake ===================================="""  # - checked


@customer_controller.route("/cakery/user/customer/Customize_Cake", methods=["GET"])
@token_required(roles=["customer"])
def view_raw_materials():
    """
    View Raw Materials for Cake Customization
    ---
    tags:
      - Customer
    summary: Retrieve a list of raw materials available for cake customization
    produces:
      - application/json
    responses:
      200:
        description: A list of raw materials
        schema:
          type: array
          items:
            type: object
            properties:
              material_id:
                type: integer
                example: 201
              name:
                type: string
                example: "Flour"
              quantity_available:
                type: integer
                example: 500
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while fetching raw materials."
            error:
              type: string
              example: "Detailed error message."
    """
    try:
        raw_materials = customer_service.view_raw_materials()
        return jsonify(raw_materials), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while fetching raw materials.",
                    "error": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""=================================== Create Custom Cake ===================================="""  # - checked


@customer_controller.route(
    "/cakery/user/customer/Customize_Cake/Create", methods=["POST"]
)  # (Customize Cake Page)
@token_required(roles=["customer"])
def create_custom_cake():
    """
    Create a Customized Cake and Add to Cart
    ---
    tags:
      - Customer
    summary: Create a customized cake based on customer preferences and add it to the cart
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details of the custom cake to be created
        required: true
        schema:
          type: object
          required:
            - cakeshape
            - cakesize
            - caketype
            - layers
          properties:
            cakeshape:
              type: string
              example: "Round"
            cakesize:
              type: string
              example: "Medium"
            caketype:
              type: string
              example: "Chocolate"
            message:
              type: string
              example: "Happy Birthday!"
            layers:
              type: array
              items:
                type: object
                properties:
                  innerFillings:
                    type: string
                    example: "Cream"
                  innerToppings:
                    type: string
                    example: "Sprinkles"
                  outerCoating:
                    type: string
                    example: "Fondant"
                  outerToppings:
                    type: string
                    example: "Cherries"
    responses:
      200:
        description: Customized cake created and added to cart successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Cake customization created successfully!"
            customizecakeid:
              type: integer
              example: 1001
      400:
        description: Bad Request - Missing required fields or validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing cakeshape"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while creating the custom cake."
            error:
              type: string
              example: "Detailed error message."
    """
    try:
        customer_email = request.user
        data = request.get_json()
        response = customer_service.create_custom_cake(customer_email, data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Error creating custom cake: {e}"}), 400


# ----------------------------------------------------------------------------------

"""=================================== Checkout ===================================="""  # - issue (voucher code)


@customer_controller.route("/cakery/user/customer/Checkout", methods=["POST"])
@token_required(roles=["customer"])
def checkout():
    """
    Checkout Customer's Cart
    ---
    tags:
      - Customer
    summary: Process the checkout of the authenticated customer's cart, optionally applying a voucher code
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Checkout details
        required: false
        schema:
          type: object
          properties:
            voucher:
              type: string
              example: "DISCOUNT20"
    responses:
      200:
        description: Checkout completed successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order placed successfully"
            order_id:
              type: integer
              example: 401
            total_amount:
              type: number
              format: float
              example: 150.75
      400:
        description: Bad Request - Missing cart or validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Cart not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "(route) error during checkout: Detailed error message."
    """
    try:
        data = request.get_json()
        customer_email = request.user
        voucher_code = data.get("voucher")
        response = customer_service.checkout(customer_email, voucher_code)
        if "error" in response:
            return jsonify(response), 400
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"(route) error during checkout: {e}"}), 500


# ----------------------------------------------------------------------------------

"""=================================== View Orders ===================================="""  # - checked


@customer_controller.route(
    "/cakery/user/customer/Orders", methods=["GET"]
)  # (Customer orders Page)
@token_required(roles=["customer"])
def view_orders():
    """
    View Customer's Orders
    ---
    tags:
      - Customer
    summary: Retrieve all orders placed by the authenticated customer
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of the authenticated customer's orders
        schema:
          type: array
          items:
            type: object
            properties:
              order_id:
                type: integer
                example: 401
              order_date:
                type: string
                format: date-time
                example: "2024-04-25T14:30:00Z"
              total_price:
                type: number
                format: float
                example: 150.75
              status:
                type: string
                example: "Delivered"
              items:
                type: array
                items:
                  type: object
                  properties:
                    product_id:
                      type: integer
                      example: 501
                    product_name:
                      type: string
                      example: "Chocolate Cake"
                    quantity:
                      type: integer
                      example: 2
                    price_at_order:
                      type: number
                      format: float
                      example: 25.50
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while fetching orders."
    """
    try:
        customer_email = request.user
        orders = customer_service.view_customer_orders(customer_email)
        return jsonify(orders), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching orders.",
                    "error_details": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""=================================== Edit Customer Data ===================================="""


@customer_controller.route("/cakery/user/customer/CheckUser", methods=["GET"])
@token_required(roles=["customer"])
def get_customer():
    """
    Get Customer
    ---
    tags:
      - Customer
    summary: Retrieve information about the authenticated customer
    security:
      - BearerAuth: []
    responses:
      200:
        description: Customer information retrieved successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User with firstname John is present in the database with completed data."
            status:
              type: string
              example: "success"
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No user found with email: example@example.com"
            status:
              type: string
              example: "error"
      422:
        description: User's data is incomplete
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User's data is incomplete."
            status:
              type: string
              example: "error"
            missing_fields:
              type: array
              items:
                type: string
                example: ["firstname", "lastname"]
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while editing user data."
            error:
              type: string
              example: "Detailed error message."
            status:
              type: string
              example: "error"
    """
    try:
        customer_email = request.user
        response, status_code = customer_service.get_user(customer_email)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while editing user data.",
                    "error": str(e),
                }
            ),
            500,
        )


@customer_controller.route("/cakery/user/customer/CheckData", methods=["GET"])
@token_required(roles=["customer"])
def get_customer_data():
    """
    Get Customer Data
    ---
    tags:
      - Customer
    summary: Retrieve detailed personal data of the authenticated customer
    security:
      - BearerAuth: []
    responses:
      200:
        description: Customer data retrieved successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User data retrieved successfully"
            status:
              type: string
              example: "success"
            data:
              type: object
              properties:
                firstname:
                  type: string
                  example: "John"
                lastname:
                  type: string
                  example: "Doe"
                phonenum:
                  type: string
                  example: "+123456789"
                addressgooglemapurl:
                  type: string
                  example: "https://maps.google.com/?q=123+Main+St"
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User not found"
            status:
              type: string
              example: "error"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while editing user data."
            error:
              type: string
              example: "Detailed error message."
            status:
              type: string
              example: "error"
    """
    try:
        customer_email = request.user
        response, status_code = customer_service.get_data(customer_email)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while editing user data.",
                    "error": str(e),
                }
            ),
            500,
        )


@customer_controller.route("/cakery/user/customer/EditData", methods=["PUT"])
@token_required(roles=["customer"])
def edit_customer_data():
    """
    Edit Customer Data
    ---
    tags:
      - Customer
    summary: Update the authenticated customer's personal data
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Customer data to be updated
        required: true
        schema:
          type: object
          properties:
            firstname:
              type: string
              example: "John"
            lastname:
              type: string
              example: "Doe"
            phonenum:
              type: string
              example: "+123456789"
            addressgooglemapurl:
              type: string
              example: "https://maps.google.com/?q=123+Main+St"
            password:
              type: string
              example: "NewSecureP@ssw0rd"
    responses:
      200:
        description: Customer data updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User's data updated successfully"
            status:
              type: string
              example: "success"
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User not found"
            status:
              type: string
              example: "error"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while editing user data"
            error:
              type: string
              example: "Detailed error message."
            status:
              type: string
              example: "error"
    """
    try:
        customer_email = request.user
        data = request.get_json()
        response, status_code = customer_service.update_data(customer_email, data)
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while editing user data.",
                    "error": str(e),
                }
            ),
            500,
        )


# --------------------------
# ----------------------------------------------------------------------------------

"""=================================== Users | Reset Password ===================================="""


@customer_controller.route("/cakery/user/customer/ResetPassword/email", methods=["POST"])
def forget_pass_email():
    """
    Forget Password - Send Email
    ---
    tags:
      - Customer
    summary: Sends a password reset email to the user
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: "user@example.com"
    responses:
      200:
        description: Password reset email sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Password reset email sent successfully"
            status:
              type: string
              example: "success"
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User not found"
            status:
              type: string
              example: "error"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Failed to send email"
            error:
              type: string
              example: "Detailed error message"
            status:
              type: string
              example: "error"
    """
    data = request.get_json()
    response, status_code = customer_service.check_user(data)  # Call check_user to send reset email
    return jsonify(response), status_code


@customer_controller.route("/cakery/user/customer/ResetPassword/CheckToken", methods=["GET"])
def forget_pass_check_token():
    """
    Forget Password - Check Token
    ---
    tags:
      - Customer
    summary: Verify the validity of a password reset token
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              token:
                type: string
                example: "reset-token"
    responses:
      200:
        description: Token is valid
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Token is valid"
            status:
              type: string
              example: "success"
      400:
        description: Invalid token
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Invalid token"
            status:
              type: string
              example: "error"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "An error occurred while verifying token"
            error:
              type: string
              example: "Detailed error message"
            status:
              type: string
              example: "error"
    """
    data = request.get_json()
    token = data.get("token")
    email = customer_service.verify_reset_token(token)  # Call verify_reset_token to check the token
    if email:
        return jsonify({
            "message": "Token is valid",
            "status": "success"
        }), 200
    else:
        return jsonify({
            "message": "Invalid token",
            "status": "error"
        }), 400


@customer_controller.route("/cakery/user/customer/ResetPassword", methods=["PUT"])
def forget_password():
    """
    Forget Password - Reset Password
    ---
    tags:
      - Customer
    summary: Reset the user's password
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
                example: "user@example.com"
              newpassword:
                type: string
                example: "NewSecurePassword123"
              newpasswordconfirm:
                type: string
                example: "NewSecurePassword123"
    responses:
      200:
        description: Password changed successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Password changed successfully"
            status:
              type: string
              example: "success"
      400:
        description: Bad request (e.g., passwords do not match)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Passwords do not match"
            status:
              type: string
              example: "error"
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User not found"
            status:
              type: string
              example: "error"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Failed to reset password"
            error:
              type: string
              example: "Detailed error message"
            status:
              type: string
              example: "error"
    """
    data = request.get_json()
    response, status_code = customer_service.change_password(data)  # Call change_password to reset the password
    return jsonify(response), status_code


"""===================================== Verify OTP ===================================="""


@customer_controller.route("/cakery/user/customer/VerifyOTP", methods=["POST"])
@token_required(roles=["customer"])
def verify_otp():
    """
    Verify OTP Code
    ---
    tags:
      - Authentication
    summary: Validate the OTP code provided by the authenticated customer
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: OTP verification details
        required: true
        schema:
          type: object
          required:
            - otp_code
          properties:
            otp_code:
              type: string
              example: "123456"
    responses:
      200:
        description: OTP validated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "OTP validated successfully"
            status:
              type: string
              example: "success"
      400:
        description: Invalid or expired OTP
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid OTP"
      500:
        description: Error validating OTP
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error validating OTP"
    """
    try:
        customer_email = request.user
        data = request.get_json()
        otp_code = data.get("otp_code")
        otp_service = customer_controller.otp_service
        response, status_code = otp_service.validate_otp(customer_email, otp_code)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Error validating OTP: {e}"}), 500


# ----------------------------------------------------------------------------------

"""===================================== My Notifications ===================================="""


@customer_controller.route("/cakery/user/customer/Notifications", methods=["GET"])
@token_required(roles=["customer"])
def view_notifications():
    """
    View Customer's Notifications
    ---
    tags:
      - Customer
    summary: Retrieve all notifications for the authenticated customer
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of customer notifications
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 601
              message:
                type: string
                example: "Your order has been delivered."
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while fetching notifications."
    """
    try:
        customer_email = request.user
        notifications = customer_service.view_notifications(customer_email)
        return jsonify(notifications), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching notifications.",
                    "error_details": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""===================================== Get Customer Name ===================================="""


@customer_controller.route("/cakery/user/customer/Name", methods=["GET"])
@token_required(roles=["customer"])
def get_customer_name():
    """
    Get Customer's Name
    ---
    tags:
      - Customer
    summary: Retrieve the authenticated customer's full name
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: The customer's full name
        schema:
          type: object
          properties:
            name:
              type: string
              example: "John Doe"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while fetching the customer name."
    """
    try:
        customer_email = request.user
        name = customer_service.get_customer_name(customer_email)
        return jsonify({"name": name}), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching the customer name.",
                    "error_details": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------

"""===================================== Customer Review ===================================="""


@customer_controller.route("/cakery/user/customer/Review", methods=["POST"])
@token_required(roles=["customer"])
def customer_review():
    """
    Submit a Review for a Product
    ---
    tags:
      - Customer
    summary: Allows a customer to submit a review with a rating for a product
    description: This endpoint allows customers to submit a review for a product. If the customer has already reviewed the product, the review is updated.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              rating:
                type: integer
                description: The rating for the product (between 1 and 5)
                example: 4
              productid:
                type: string
                description: The ID of the product being reviewed
                example: "prod12345"
    responses:
      200:
        description: Review updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User rating updated successfully"
                status:
                  type: string
                  example: "success"
      201:
        description: Review added successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User rating added successfully"
                status:
                  type: string
                  example: "success"
      400:
        description: Bad request (e.g., invalid rating or missing parameters)
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Rating must be between 1 and 5"
                status:
                  type: string
                  example: "error"
      404:
        description: Customer or product not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Customer does not exist"
                status:
                  type: string
                  example: "error"
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "An error occurred"
                error:
                  type: string
                  example: "Detailed error message"
                status:
                  type: string
                  example: "error"
    security:
      - BearerAuth: []
    """
    try:
        customer_email = request.user
        data = request.get_json()
        rating = data.get("rating")
        product_id = data.get("productid")
        response, status_code = customer_service.add_review(
            customer_email, rating, product_id
        )
        return jsonify(response), status_code
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching the customer name.",
                    "error_details": str(e),
                }
            ),
            500,
        )


# ----------------------------------------------------------------------------------
