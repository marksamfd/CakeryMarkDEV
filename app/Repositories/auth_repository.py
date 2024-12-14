from flask import jsonify
from app.models import CustomerUser, DeliveryUser, Admin, BakeryUser
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from argon2 import PasswordHasher
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


ph = PasswordHasher()


class AuthRepository:
    ''' ============================ Hashing password during sign up =============================== '''

    def hash_password(self,password):
        return ph.hash(password)
    # -------------------------------------------------------------------------------    

    ''' ============================ Verify the password during sign-in =============================== '''

    def verify_password(self,stored_password, provided_password):
        try:
        # Argon2 will automatically verify the password hash
            ph.verify(stored_password, provided_password)
            return True
        except Exception:
            return False
    # -------------------------------------------------------------------------------    

    ''' ============================ Adding new customer =============================== '''

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
        if not customer_email or not password or not firstname or not lastname or not phonenum:
            return {"message": "Missing required fields", "status": "error"}, 400

        try:
            # Check if user already exists
            domain = customer_email.split("@")[1]
            if domain in ["cakery_baker.com", "cakery_admin.com", "cakery_delivery.com"]:
                return {"message": "Can't sign up for staff", "status": "error"}, 409

            result = CustomerUser.query.filter_by(customeremail=customer_email).first()
            if result:
                return {"message": "User already exists with this email", "status": "error"}, 409

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
                createdat=createdat
                )

            db.session.add(new_customer)
            db.session.commit()

            return {"message": "User signed up successfully", "status": "success"}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while signing up", "error": str(e), "status": "error"}, 500

    # -------------------------------------------------------------------------------    

    ''' ============================ User sign in =============================== '''

    def user_sign_in(self,data):

        email = data.get("email")
        password = data.get("password")

        # Validate required fields
        if not email or not password:
            return {
            "message": "Email and password are required",
            "status": "error"
            }, 400

        # Extract user domain
        domain = email.split("@")[1] if "@" in email else None

        if not domain:
            return {
            "message": "Invalid email format",
            "status": "error"
            }, 400

        role = None
        user = None

        # Define the queries for different user roles
        if domain == "cakery_admin.com":
            user = Admin.query.filter_by(adminemail=email).first()
            role = "admin"
        elif domain == "cakery_baker.com":
            user = BakeryUser.query.filter_by(bakeryemail=email).first()
            role = "baker"
            name = user.firstname
        elif domain == "gmail.com":
            user = CustomerUser.query.filter_by(customeremail=email).first()
            role = "customer"
            name = user.firstname
        elif domain == "cakery_delivery.com":
            user = DeliveryUser.query.filter_by(deliveryemail=email).first()
            role = "delivery"
            name = user.firstname
        else:
            return {
                "message": "Invalid email domain",
                "status": "error"
            }, 400

        try:
            # User not found
            if not user:
                return {
                    "message": "User not found",
                    "status": "error"
                }, 401

            # Compare the stored password and the input password
            stored_password = user.password
            #stored_password == password
            """ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ To be Edited later ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Caution ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            ''' I commented the condition above because the password is hashed and can't be compared directly '''
            #if self.verify_password(stored_password, password):
            # Create JWT token with role as an additional claim
            additional_claims = {"role": role}
            access_token = create_access_token(identity=email, additional_claims=additional_claims)
            return {
                    "message": "Sign-in successful",
                    "status": "success",
                    "firstname":name,
                    "role": role,
                    "access_token": access_token
                }, 200
            # else:
            #     return {
            #         "message": "Wrong Password",
            #         "status": "error"
            #     }, 401



        except Exception as e:
            return {
                "message": "An error occurred during sign-in",
                "error": str(e),
                "status": "error"
            }, 500

    # -------------------------------------------------------------------------------  


    def change_password(self,data):
        email = data.get("email")
        domain = email.split("@")[1]

        
        if domain == "cakery_baker.com":
            user = BakeryUser.query.filter_by(bakeryemail=email).first()
            role = "baker"
        elif domain == "gmail.com":
            user = CustomerUser.query.filter_by(customeremail=email).first()
            role = "customer"
        elif domain == "cakery_delivery.com":
            user = DeliveryUser.query.filter_by(deliveryemail=email).first()
            role = "delivery"
        else:
            return {
                "message": "Invalid email domain",
                "status": "error"
            }, 400

        try:
            if not user:
                return {
                    "message": "User not found please sign up",
                    "status": "error"
                }, 401

            new_pass = data.get("newpassword")
            new_pass_confirm = data.get("newpasswordconfirm")  # Fixed typo here

            # Check if passwords match
            if new_pass != new_pass_confirm:
                return {
                    "message": "Passwords do not match",
                    "status": "error"
                }, 400

            # Assuming you want to hash the password before saving it
            hashed_password = self.hash_password(new_pass)  # Replace with actual hashing logic

            # Update the user's password
            if role == "baker":
                user.bakerypassword = hashed_password
            elif role == "customer":
                user.customerpassword = hashed_password
            elif role == "delivery":
                user.deliverypassword = hashed_password
        
            # Commit the changes to the database
            db.session.commit()

            return {
                "message": "Password changed successfully",
                "status": "success"
            }, 200

        except Exception as e:
            return {
                "message": f"An error occurred: {str(e)}",
                "status": "error"
            }, 500


        