from flask import Blueprint, jsonify, request
from app.Services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import CustomerUser
from app.db import db
from app.Middlewares.auth_middleware import token_required
from firebase_admin import messaging


auth_controller = Blueprint("auth_controller", __name__)
auth_service = AuthService()

"""=================================== Customer | SignUp ===================================="""


@auth_controller.route("/cakery/user/SignUp", methods=["POST"])
def signup():
    """
    Customer Sign Up
    ---
    tags:
      - Authentication
    summary: Register a new customer user
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Customer registration details
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - firstname
            - lastname
            - phonenum
          properties:
            email:
              type: string
              example: john.doe@example.com
            password:
              type: string
              example: SecureP@ssw0rd
            firstname:
              type: string
              example: John
            lastname:
              type: string
              example: Doe
            phonenum:
              type: string
              example: "+123456789"
            addressgooglemapurl:
              type: string
              example: "https://maps.google.com/?q=123+Main+St"
    responses:
      201:
        description: User signed up successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: User signed up successfully
            status:
              type: string
              example: success
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            message:
              type: string
              example: Missing required fields
            status:
              type: string
              example: error
      409:
        description: User already exists or cannot sign up for staff
        schema:
          type: object
          properties:
            message:
              type: string
              example: User already exists with this email
            status:
              type: string
              example: error
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: An error occurred while signing up
            error:
              type: string
              example: Detailed error message
            status:
              type: string
              example: error
    """
    data = request.get_json()
    response, status_code = auth_service.add_new_user(data)
    return jsonify(response), status_code


# -------------------------------------------------------------------------------

"""=================================== Users | SignIn ===================================="""


@auth_controller.route("/cakery/user/SignIn", methods=["POST"])
def signin():
    """
    User Sign In
    ---
    tags:
      - Authentication
    summary: Authenticate a user and provide a JWT token
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: User login credentials
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: john.doe@example.com
            password:
              type: string
              example: SecureP@ssw0rd
    responses:
      200:
        description: Sign-in successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: Sign-in successful
            status:
              type: string
              example: success
            firstname:
              type: string
              example: John
            role:
              type: string
              example: customer
            access_token:
              type: string
              example: eyJ0eXAiOiJKV1QiLCJhbGciOiJI...
      400:
        description: Invalid input or email format
        schema:
          type: object
          properties:
            message:
              type: string
              example: Email and password are required
            status:
              type: string
              example: error
      401:
        description: Unauthorized - User not found or wrong password
        schema:
          type: object
          properties:
            message:
              type: string
              example: User not found
            status:
              type: string
              example: error
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            message:
              type: string
              example: An error occurred during sign-in
            error:
              type: string
              example: Detailed error message
            status:
              type: string
              example: error
    """
    data = request.get_json()
    response, status_code = auth_service.sign_user_in(data)
    return jsonify(response), status_code


# -------------------------------------------------------------------------------


"""=================================== Test Auth Middleware ===================================="""


@auth_controller.route("/cakery/user/Profile", methods=["GET"])
@token_required(roles=["admin", "customer"])
def get_profile():
    """
    Get User Profile
    ---
    tags:
      - Authentication
    summary: Retrieve the profile of the authenticated user
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: Successfully retrieved user profile
        schema:
          type: object
          properties:
            message:
              type: string
              example: Welcome john.doe@example.com, your role is customer
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          type: object
          properties:
            message:
              type: string
              example: Missing Authorization Header
            status:
              type: string
              example: error
    """
    return jsonify(
        {"message": f"Welcome {request.user}, your role is {request.role}"})


'''=================================== Customer - Notification ==================================='''
@auth_controller.route("/cakery/user/customer/NotificationToken", methods=["POST"])
@jwt_required()
def update_fcm_token():
    """
    Update Customer's FCM Token
    ---
    tags:
      - Customer
    summary: Update the customer's Firebase Cloud Messaging token
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Customer FCM token
        required: true
        schema:
          type: object
          properties:
            fcm_token:
              type: string
              example: "your_fcm_token"
    responses:
      200:
        description: Token updated successfully
      400:
        description: Missing token or invalid input
      500:
        description: Internal Server Error
    """
    try:
        customer_email = get_jwt_identity()
        data = request.get_json()
        fcm_token = data.get("fcm_token")

        if not fcm_token:
            return jsonify({"error": "FCM token is required"}), 400

        customer = CustomerUser.query.filter_by(customeremail=customer_email).first()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        customer.fcm_token = fcm_token
        db.session.commit()
        return jsonify({"message": "FCM token updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating FCM token: {e}"}), 500



