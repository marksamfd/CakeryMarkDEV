from flask import Blueprint,request,jsonify, make_response, current_app
import jwt
from argon2 import PasswordHasher
from sqlalchemy.sql import text

#from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime,timedelta
from functools import wraps


auth = Blueprint("auth",__name__)
ph = PasswordHasher()

# Hash password to be stored in database
def hash_password(password):
    return ph.hash(password)

# Verify the password during sign in 
def verify_password(stored_password, provided_password):
    try:
        # Argon2 will automatically verify the password hash
        ph.verify(stored_password, provided_password)
        return True
    except:
        return False



# SignUp Route 
@auth.route("/App/User/SignUp", methods=["POST"])
def sign_up():
    data = request.get_json() 
    db = current_app.extensions['sqlalchemy'] 
    
    # Extract required fields
    email = data.get('email')
    password = data.get("password")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    phonenum = data.get("phonenum")
    addressgooglemapurl = data.get("addressgooglemapurl")
    createdat = data.get("createdat", datetime.utcnow())

    # Handle missing input fields case 
    if not email or not password or not firstname or not lastname or not phonenum:
        return jsonify({
            "message": "Missing required fields",
            "status": "error"
        }), 400

    try:
        # Check if user already exists
        query_check_user = text("SELECT 1 FROM customeruser WHERE customeremail = :email")
        result = db.session.execute(query_check_user, {'email': email}).fetchone()

        if result:
            return jsonify({
                "message": "User already exists with this email",
                "status": "error"
            }), 409

        # Hash the password
        hashed_password = hash_password(password)

        # If user is not present insert the new user
        query_insert_user = text("""
            INSERT INTO customeruser (customeremail, password, firstname, lastname, phonenum, addressgooglemapurl, createdat)
            VALUES (:email, :password, :firstname, :lastname, :phonenum, :addressgooglemapurl, :createdat)
        """)
        db.session.execute(query_insert_user, {
            'email': email,
            'password': hashed_password,
            'firstname': firstname,
            'lastname': lastname,
            'phonenum': phonenum,
            'addressgooglemapurl': addressgooglemapurl,
            'createdat': createdat
        })
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


# Generate JWT token with role 
def generate_jwt(email, role, expires_in=3600):

    expiration_time = datetime.utcnow() + timedelta(seconds=expires_in)

    # Define the token payload
    payload = {
        "sub": email,  # Subject (the user for whom the token is issued)
        "role": role,  # The role of the user
        "exp": expiration_time,  # Expiration time of the token
        "iat": datetime.utcnow()  # Issued at time
    }

    # Encode the JWT with the payload and secret key
    SECRET_KEY = current_app.config["SECRET_KEY"]
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

# @token_required to manage the access to the secured pages and validate the token 
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing", "status": "error"}), 403

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired", "status": "error"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "status": "error"}), 401

        return f(payload, *args, **kwargs)
    return decorated_function


# Sign in route 
@auth.route("/App/User/SignIn", methods=["POST"])
def sign_in():
    db = current_app.extensions['sqlalchemy']
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Validate required fields
    if not email or not password:
        return jsonify({
            "message": "Email and password are required",
            "status": "error"
        }), 400

    domain = email.split("@")[1] # extract user domain 

    user_query = None
    role = None

    # Define the queries for different user roles
    if domain == "cakery_admin.com":
        user_query = text("SELECT adminemail, password FROM admin WHERE adminemail = :email")
        role = "admin"
    elif domain == "cakery_baker.com":
        user_query = text("SELECT bakeryemail, password FROM bakeryuser WHERE bakeryemail = :email")
        role = "baker"
    elif domain == "gmail.com":
        user_query = text("SELECT customeremail, password FROM customeruser WHERE customeremail = :email")
        role = "customer"

    elif domain == "cakery_delivery.com":
        user_query = text("SELECT deliveryemail, password FROM deliveryuser WHERE deliveryemail = :email")
        role = "delivery"
    else:
        return jsonify({
            "message": "Invalid email domain",
            "status": "error"
        }), 400

    try:
        # Execute the query to fetch user details
        result = db.session.execute(user_query, {"email": email}).fetchone()

        # User is not found 
        if not result:
            return jsonify({
                "message": "User not found or incorrect password",
                "status": "error"
            }), 401

        db_email, db_password = result

        # Encrypt the input password and compare

        stored_password = result[1] # stored password for current user in database 
        
        # Verify the password using Argon2
        if verify_password(stored_password, password):
            return jsonify({
                "message": "Sign-in successful",
                "status": "success"
            }), 200
        else:
            return jsonify({
                "message": stored_password,
                "status": "error"
            }), 401
    except Exception as e:
        return jsonify({
            "message": "An error occurred during sign-in",
            "error": str(e),
            "status": "error"
        }), 500