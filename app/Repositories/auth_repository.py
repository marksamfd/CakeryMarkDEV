from flask import jsonify
from app.models import CustomerUser, DeliveryUser, Admin, BakeryUser, Cart
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from argon2 import PasswordHasher
from datetime import datetime
from flask_jwt_extended import create_access_token
import re

ph = PasswordHasher()


class AuthRepository:
    """============================ Hashing password during sign up ==============================="""

    def hash_password(self, password):
        return ph.hash(password)

    # -------------------------------------------------------------------------------

    """ ============================ Verify the password during sign-in =============================== """

    def verify_password(self, stored_password, provided_password):
        try:
            # Argon2 will automatically verify the password hash
            ph.verify(stored_password, provided_password)
            return True
        except Exception:
            return False

    # -------------------------------------------------------------------------------

    """ ============================ Adding new customer =============================== """

    def add_user(self, data):
        # Extract required fields
        customer_email = data.get("email")
        password = data.get("password")
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        phonenum = data.get("phonenum")
        addressgooglemapurl = data.get("addressgooglemapurl")
        createdat = data.get("createdat", datetime.utcnow())

        # Handle missing input fields
        if (
            not customer_email
            or not password
            or not firstname
            or not lastname
            or not phonenum
        ):
            return {"message": "Missing required fields", "status": "error"}, 400

        try:
            # Validate email format
            if not self.is_valid_email(customer_email):
                return {"message": "Invalid email format", "status": "error"}, 400

            # Check if user already exists
            domain = customer_email.split("@")[1]
            if domain in ["cakerybaker.com", "cakeryadmin.com", "cakerydelivery.com"]:
                return {"message": "Can't sign up for staff", "status": "error"}, 409

            if domain not in ["gmail.com"]:
                return {"message": "Invalid email domain", "status": "error"}, 400

            # Check if the email is already used
            existing_user = CustomerUser.query.filter_by(
                customeremail=customer_email
            ).first()
            if existing_user:
                return {
                    "message": "User already exists with this email",
                    "status": "error",
                }, 409

            # Hash the password
            hashed_password = self.hash_password(password)

            # Insert the new user
            new_customer = CustomerUser(
                customeremail=customer_email,
                password=hashed_password,
                firstname=firstname,
                lastname=lastname,
                phonenum=phonenum,
                addressgooglemapurl=addressgooglemapurl,
                createdat=createdat,
            )

            db.session.add(new_customer)
            db.session.commit()

            # Create an associated cart
            new_cart = Cart(customeremail=customer_email)
            db.session.add(new_cart)
            db.session.commit()

            return {"message": "User signed up successfully", "status": "success"}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "An error occurred while signing up",
                "status": "error",
                "error": str(e),
            }, 500

    # -------------------------------------------------------------------------------

    """ ============================ User sign in =============================== """

    def user_sign_in(self, data):
        email = data.get("email")
        password = data.get("password")

        # Validate required fields
        if not email or not password:
            return {
                "message": "Email and password are required",
                "status": "error",
            }, 400

        # Validate email format
        if not self.is_valid_email(email):
            return {"message": "Invalid email format", "status": "error"}, 400

        # Extract domain from email
        domain = email.split("@")[1] if "@" in email else None
        if not domain:
            return {"message": "Invalid email format", "status": "error"}, 400

        role = None
        user = None
        name = None

        # Define the queries for different user roles based on email domain
        if domain == "cakeryadmin.com":
            user = Admin.query.filter_by(adminemail=email).first()
            role = "admin"
        elif domain == "cakerybaker.com":
            user = BakeryUser.query.filter_by(bakeryemail=email).first()
            role = "baker"
            name = user.firstname if user else None
        elif domain == "gmail.com":
            user = CustomerUser.query.filter_by(customeremail=email).first()
            role = "customer"
            name = user.firstname if user else None
        elif domain == "cakerydelivery.com":
            user = DeliveryUser.query.filter_by(deliveryemail=email).first()
            role = "delivery"
            name = user.firstname if user else None
        else:
            return {"message": "Invalid email domain", "status": "error"}, 400

        try:
            # User not found
            if not user:
                return {"message": "User not found", "status": "error"}, 401

            # Verify password
            
            if not self.verify_password(user.password, password):
                return {"message": "Wrong password", "status": "error"}, 401

            # Create JWT token with role as an additional claim
            additional_claims = {"role": role}
            access_token = create_access_token(
                identity=email, additional_claims=additional_claims
            )

            return {
                "message": "Sign-in successful",
                "status": "success",
                "firstname": name,
                "role": role,
                "access_token": access_token,
            }, 200

        except Exception as e:
            return {
                "message": "An error occurred during sign-in",
                "status": "error",
                "error": str(e),
            }, 500

    # -------------------------------------------------------------------------------

    """ ============================ Email Format Validation =============================== """

    def is_valid_email(self, email):
        """Validate email format using regex"""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None
