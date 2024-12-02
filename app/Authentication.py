from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import *
from argon2 import PasswordHasher
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

auth_routes = Blueprint("auth_routes", __name__)
ph = PasswordHasher()

# Hash password to be stored in the database
def hash_password(password):
    return ph.hash(password)

# Verify the password during sign-in
def verify_password(stored_password, provided_password):
    try:
        # Argon2 will automatically verify the password hash
        ph.verify(stored_password, provided_password)
        return True
    except Exception:
        return False

# Sign-up route
@auth_routes.route("/App/User/SignUp", methods=["POST"])
def sign_up():
    data = request.get_json()

    # Extract required fields
    email = data.get('email')
    password = data.get("password")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    phonenum = data.get("phonenum")
    addressgooglemapurl = data.get("addressgooglemapurl")
    createdat = data.get("createdat", datetime.utcnow())

    # Handle missing input fields
    if not email or not password or not firstname or not lastname or not phonenum:
        return jsonify({
            "message": "Missing required fields",
            "status": "error"
        }), 400

    try:
        # Check if user already exists
        result = CustomerUser.query.filter_by(customeremail=email).first()

        if result:
            return jsonify({
                "message": "User already exists with this email",
                "status": "error"
            }), 409

        # Hash the password
        hashed_password = hash_password(password)

        # Insert the new user
        new_customer = CustomerUser(
            customeremail=email,
            password=hashed_password,
            firstname=firstname,
            lastname=lastname,
            phonenum=phonenum,
            addressgooglemapurl=addressgooglemapurl,
            createdat=createdat
        )

        db.session.add(new_customer)
        db.session.commit()

        return jsonify({
            "message": "User signed up successfully",
            "status": "success"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "An error occurred while signing up",
            "error": str(e),
            "status": "error"
        }), 500

# Sign-in route
@auth_routes.route("/App/User/SignIn", methods=["POST"])
def sign_in():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Validate required fields
    if not email or not password:
        return jsonify({
            "message": "Email and password are required",
            "status": "error"
        }), 400

    # Extract user domain
    domain = email.split("@")[1] if "@" in email else None

    if not domain:
        return jsonify({
            "message": "Invalid email format",
            "status": "error"
        }), 400

    role = None
    user = None

    # Define the queries for different user roles
    if domain == "cakery_admin.com":
        user = Admin.query.filter_by(adminemail=email).first()
        role = "admin"
    elif domain == "cakery_baker.com":
        user = BakeryUser.query.filter_by(bakeryemail=email).first()
        role = "baker"
    elif domain == "gmail.com":
        user = CustomerUser.query.filter_by(customeremail=email).first()
        role = "customer"
    elif domain == "cakery_delivery.com":
        user = DeliveryUser.query.filter_by(deliveryemail=email).first()
        role = "delivery"
    else:
        return jsonify({
            "message": "Invalid email domain",
            "status": "error"
        }), 400

    try:
        # User not found
        if not user:
            return jsonify({
                "message": "User not found",
                "status": "error"
            }), 401

        # Compare the stored password and the input password
        stored_password = user.password
        #verify_password(stored_password, password)
        if stored_password == password:
            # Create JWT token with role as an additional claim
            additional_claims = {"role": role}
            access_token = create_access_token(identity=email, additional_claims=additional_claims)
            return jsonify({
                "message": "Sign-in successful",
                "status": "success",
                "access_token": access_token
            }), 200
        else:
            return jsonify({
                "message": "Wrong Password",
                "status": "error"
            }), 401

    except Exception as e:
        return jsonify({
            "message": "An error occurred during sign-in",
            "error": str(e),
            "status": "error"
        }), 500
