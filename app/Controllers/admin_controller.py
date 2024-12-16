from flask import Blueprint, request, jsonify
from app.Services.admin_service import AdminService
from app.Services.order_service import OrderService
from flask_jwt_extended import jwt_required

admin_controller = Blueprint("admin_controller", __name__)

order_service = OrderService()
admin_service = AdminService()

'''=================================== Admin | Users ===================================='''

@admin_controller.route("/cakery/user/admin/ViewCustomers", methods=["GET"])  # -- checked
@jwt_required()
def view_customers():
    """
    View all customers
    ---
    tags:
      - Admin
    summary: Get all customer details
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of customers
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                example: John Doe
              email:
                type: string
                example: john.doe@example.com
              phone:
                type: string
                example: "+123456789"
      401:
        description: Unauthorized
    """

    customers = admin_service.get_customers()
    return jsonify(customers), 200


'''=================================== Admin | Staff ===================================='''
# ----------------------------- View Staff -----------------------------
@admin_controller.route("/cakery/user/admin/Staff/View", methods=["GET"])  # -- checked
@jwt_required()
def view_staff():
    """
    View all staff users
    ---
    tags:
      - Admin
    summary: Get all staff details
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of staff members
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                example: Jane Smith
              email:
                type: string
                example: jane.smith@example.com
              phone:
                type: string
                example: "+987654321"
              role:
                type: string
                example: baker
      401:
        description: Unauthorized
    """

    staff = admin_service.get_users()
    return jsonify(staff), 200

# ----------------------------- Add Staff -----------------------------
@admin_controller.route("/cakery/user/admin/Staff/Add", methods=["POST"])
@jwt_required()
def add_staff():
    """
    Add a new staff user
    ---
    tags:
      - Admin
    summary: Add a staff member
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Staff user details
        required: true
        schema:
          type: object
          properties:
            firstname:
              type: string
              example: John
            lastname:
              type: string
              example: Doe
            email:
              type: string
              example: john.doe@example.com
            phone:
              type: string
              example: "+123456789"
            password:
              type: string
              example: secretpassword
            role:
              type: string
              enum: [baker, delivery]
              example: baker
    responses:
      200:
        description: Staff member added successfully
      400:
        description: Invalid role
      500:
        description: Internal Server Error
    """

    try:
        data = request.get_json()
        response = admin_service.add_user(data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f" (route) can't add a staff user: {e}"}), 500
    

# ----------------------------- Delete Staff -----------------------------
@admin_controller.route("/cakery/user/admin/Staff/Delete", methods=["DELETE"])
@jwt_required()
def delete_staff():
    """
    Delete a staff user
    ---
    tags:
      - Admin
    summary: Delete a staff member by email and role
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Staff user identification
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: jane.smith@example.com
            role:
              type: string
              enum: [baker, delivery]
              example: baker
    responses:
      200:
        description: Staff member deleted successfully
      400:
        description: Invalid role
      500:
        description: Internal Server Error
    """

    data = request.get_json()
    response, status_code = admin_service.delete_user(data)
    return jsonify(response), status_code


@admin_controller.route("/cakery/user/admin/Products", methods=["GET"])
@jwt_required()
def view_products():
    """
    View all products and raw materials
    ---
    tags:
      - Admin
    summary: Get all products and raw materials
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of products and raw materials
        schema:
          type: array
          items:
            type: object
            properties:
              price:
                type: number
                example: 10.99
              quantity:
                type: integer
                example: 50
      401:
        description: Unauthorized
    """

    products = admin_service.get_products()
    return jsonify(products), 200

# ----------------------------- Edit Product -----------------------------

@admin_controller.route("/cakery/user/admin/Products/edit", methods=["PUT"])
@jwt_required()
def edit_products():
    """
    Edit product or raw material prices
    ---
    tags:
      - Admin
    summary: Update product or raw material price
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Product or raw material details to update
        required: true
        schema:
          type: object
          properties:
            product_id:
              type: integer
              example: 1
            rawItem:
              type: string
              example: Flour
            price:
              type: number
              example: 15.99
    responses:
      200:
        description: Product or raw material updated successfully
      400:
        description: Invalid data
      500:
        description: Internal Server Error
    """

    data = request.get_json()
    response, status_code = admin_service.edit_product(data)
    return jsonify(response), status_code

# ----------------------------- Add Voucher -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers/Add", methods=["POST"])
@jwt_required()
def add_voucher():
    """
    Add a new voucher
    ---
    tags:
      - Admin
    summary: Add a voucher
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Voucher details
        required: true
        schema:
          type: object
          properties:
            discount:
              type: number
              example: 20
    responses:
      200:
        description: Voucher added successfully
      400:
        description: Invalid data
      500:
        description: Internal Server Error
    """

    data = request.get_json()
    response, status_code = admin_service.add_voucher(data)
    return jsonify(response), status_code

# ----------------------------- Edit Voucher -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers/Edit", methods=["PUT"])
@jwt_required()
def edit_voucher():
    """
    Edit an existing voucher
    ---
    tags:
      - Admin
    summary: Update a voucher's discount
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Voucher details to update
        required: true
        schema:
          type: object
          properties:
            voucher_id:
              type: integer
              example: 101
            discount:
              type: number
              example: 25
    responses:
      200:
        description: Voucher updated successfully
      400:
        description: Invalid data
      500:
        description: Internal Server Error
    """

    data = request.get_json()
    response, status_code = admin_service.edit_voucher(data)
    return jsonify(response), status_code

# ----------------------------- Delete Voucher -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers/Delete", methods=["DELETE"])
@jwt_required()
def delete_voucher():
    """
    Delete a voucher
    ---
    tags:
      - Admin
    summary: Remove a voucher by its ID
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Voucher identification
        required: true
        schema:
          type: object
          properties:
            voucher_id:
              type: integer
              example: 101
    responses:
      200:
        description: Voucher deleted successfully
      400:
        description: Invalid data
      500:
        description: Internal Server Error
    """

    data = request.get_json()
    response, status_code = admin_service.delete_voucher(data)
    return jsonify(response), status_code
# ----------------------------- View Vouchers -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers", methods=["GET"])
@jwt_required()
def view_vouchers():
    """
    View all vouchers
    ---
    tags:
      - Admin
    summary: Retrieve a list of all vouchers
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: Vouchers retrieved successfully
      401:
        description: Unauthorized
    """

    vouchers = admin_service.get_vouchers()
    return jsonify(vouchers), 200

'''=================================== Admin | Dashboard ===================================='''

@admin_controller.route("/cakery/user/admin/Dashboard", methods=["GET"])
@jwt_required()
def view_dashboard():
  try:
        response = admin_service.dashboard_data()  # Ensure this call works
        return jsonify(response), 200  # Return a proper JSON response with HTTP status code 200
  except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500  # Return an error response with status code 500