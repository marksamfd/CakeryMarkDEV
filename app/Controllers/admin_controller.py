from flask import Blueprint, request, jsonify
from app.Services.admin_service import AdminService
from app.Services.order_service import OrderService
from flask_jwt_extended import jwt_required
from app.Middlewares.auth_middleware import token_required

admin_controller = Blueprint("admin_controller", __name__)

order_service = OrderService()
admin_service = AdminService()

"""=================================== Admin | Users ===================================="""


@admin_controller.route(
    "/cakery/user/admin/ViewCustomers", methods=["GET"]
)  # -- checked
@token_required(roles=['admin'])
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


"""=================================== Admin | Staff ===================================="""


# ----------------------------- View Staff -----------------------------
@admin_controller.route("/cakery/user/admin/Staff/View",
                        methods=["GET"])  # -- checked
@token_required(roles=['admin'])
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
@token_required(roles=['admin'])
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
@token_required(roles=['admin'])
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
    try:
        response = admin_service.delete_user(data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify(
            {"error": f" (route) can't delete a staff user: {e}"}), 500


@admin_controller.route("/cakery/user/admin/Products", methods=["GET"])
@token_required(roles=['admin'])
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
@token_required(roles=['admin'])
def edit_products():
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
        description: Details of the voucher to edit
        required: true
        schema:
          type: object
          properties:
            voucher_code:
              type: string
              example: VOUCHER123
            discount:
              type: number
              example: 25
    responses:
      200:
        description: Voucher updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Voucher updated successfully"
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid voucher data"
      404:
        description: Voucher not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Voucher not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while updating the voucher"
    """
    data = request.get_json()
    response, status_code = admin_service.edit_product(data)
    return jsonify(response), status_code


# ----------------------------- Add Voucher -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers/Add", methods=["POST"])
@token_required(roles=['admin'])
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
        description: Details of the voucher to add
        required: true
        schema:
          type: object
          properties:
            voucher_code:
              type: string
              example: VOUCHER123
            discount:
              type: number
              example: 20
    responses:
      200:
        description: Voucher added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Voucher added successfully"
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid voucher data"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while adding the voucher"
    """
    data = request.get_json()
    response, status_code = admin_service.add_voucher(data)
    return jsonify(response), status_code


# ----------------------------- Edit Voucher -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers/Edit", methods=["PUT"])
@token_required(roles=['admin'])
def edit_voucher():
    """
    Delete a voucher
    ---
    tags:
      - Admin
    summary: Remove a voucher by its code
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details of the voucher to delete
        required: true
        schema:
          type: object
          properties:
            voucher_code:
              type: string
              example: VOUCHER123
    responses:
      200:
        description: Voucher deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Voucher deleted successfully"
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid voucher code"
      404:
        description: Voucher not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Voucher not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while deleting the voucher"
    """
    data = request.get_json()
    response, status_code = admin_service.edit_voucher(data)
    return jsonify(response), status_code


# ----------------------------- Delete Voucher -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers/Delete",
                        methods=["DELETE"])
@token_required(roles=['admin'])
def delete_voucher():
    """
    Delete a voucher
    ---
    tags:
      - Admin
    summary: Remove a voucher by its code
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details of the voucher to delete
        required: true
        schema:
          type: object
          properties:
            voucher_code:
              type: string
              example: VOUCHER123
    responses:
      200:
        description: Voucher deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Voucher deleted successfully"
      400:
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid voucher code"
      404:
        description: Voucher not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Voucher not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An error occurred while deleting the voucher"
    """
    data = request.get_json()
    response, status_code = admin_service.delete_voucher(data)
    return jsonify(response), status_code


# ----------------------------- View Vouchers -----------------------------
@admin_controller.route("/cakery/user/admin/Vouchers", methods=["GET"])
@token_required(roles=['admin'])
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


"""=================================== Admin | Dashboard ===================================="""


@admin_controller.route("/cakery/user/admin/Dashboard", methods=["GET"])
@token_required(roles=['admin'])
def view_dashboard():
    """
    View the admin dashboard
    ---
    tags:
      - Admin
    summary: Get the admin dashboard data
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: Admin dashboard data retrieved successfully
      401:
        description: Unauthorized
      500:
        description: Internal Server Error
    """
    try:
        response = admin_service.dashboard_data()  # Ensure this call works
        return (
            jsonify(response),
            200,
        )  # Return a proper JSON response with HTTP status code 200
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {e}")
        return (
            jsonify({"status": "error", "message": str(e)}),
            500,
        )  # Return an error response with status code 500
