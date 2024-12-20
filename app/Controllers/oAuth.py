from flask import Blueprint, redirect, request, jsonify
import os
from app.models import CustomerUser, DeliveryUser, Admin, BakeryUser, Cart
from app.db import db
from datetime import datetime
from flask_jwt_extended import create_access_token
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

# Logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Google OAuth credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv("REDIRECT_URI")
#SCOPE = os.getenv("SCOPE")
SCOPE = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"


# OAuth Blueprint
google_oauth = Blueprint('google_oauth', __name__)

# Initiate Google Sign-In and taking permissions from user 
@google_oauth.route('/App/User/Google-Signin')
def google_signin():
    """
    Redirects the user to Google's OAuth consent screen where they will
    authorize the application to access their Google profile and email.
    """
    # Construct the Google OAuth URL with necessary parameters
    google_oauth_url = (
        f'https://accounts.google.com/o/oauth2/v2/auth?'
        f'client_id={CLIENT_ID}&'  
        f'redirect_uri={REDIRECT_URI}&'  # The redirect URI after successful login
        f'scope={SCOPE}&'  # Permissions to request from the user (email, profile, openid)
        f'response_type=code&'  # Will be exchanged with the access token 
        f'access_type=offline'
    )

    # Log the URL for debugging purposes
    logging.debug(f"Redirecting to Google OAuth URL: {google_oauth_url}")

    # Redirect the user to the Google OAuth URL to begin the sign-in process
    return redirect(google_oauth_url)

# Google oAuth url for sign in 
@google_oauth.route('/App/User/Google-Callback')
def google_callback():
    """
    Handles the callback from Google after the user authorizes the application. 
    It exchanges the authorization code for an access token and fetches the user's email.
    """
    auth_code = request.args.get('code')

    if not auth_code:
        logging.error("Authorization code not found in callback request.")
        return jsonify({"error": "Authorization code not found"}), 400

    logging.debug(f"Received authorization code: {auth_code}")

    # Exchange authorization code for tokens
    token_url = 'https://oauth2.googleapis.com/token'
    payload = {
        'code': auth_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        scope = token_data.get("scope")
        logging.info("Successfully obtained access token.")

        # Use the access token to fetch the user's profile information
        userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(userinfo_url, headers=headers)

        if userinfo_response.status_code == 200:
            userinfo = userinfo_response.json()
            email = userinfo.get("email")  # Extract the email address
            name = userinfo.get("name")  # Extract the name if needed
            
            # Validate email and name
            if not email or not name:
                return jsonify({"error": "User information is incomplete"}), 400
            
            logging.info(f"User email: {email}, User name: {name}")

            # Extract domain
            domain = email.split("@")[1] if "@" in email else None
            if not domain:
                return jsonify({"message": "Invalid email format", "status": "error"}), 400

            # Check if user already exists
            additional_claims = {"role": 'customer'}
            jwt_access_token = create_access_token(identity=email, additional_claims=additional_claims)
            existing_user = CustomerUser.query.filter_by(customeremail=email).first()
            if existing_user:
                return jsonify({
                    "message": "User already exists with this email",
                    "status": "error",
                    "jwt_access_token": jwt_access_token,
                    "refresh_token": refresh_token,
                    "expires_in": expires_in,
                    "scope": scope
                }), 409

            # Split name into first and last name
            name_parts = name.split(" ", 1)
            firstname = name_parts[0]
            lastname = name_parts[1] if len(name_parts) > 1 else ""

            # Current timestamp for createdat
            createdat = datetime.utcnow()

            # Add new user to database
            new_customer = CustomerUser(
                customeremail=email,
                firstname=firstname,
                lastname=lastname,
                createdat=createdat
            )
            
            try:
                db.session.add(new_customer)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logging.error(f"Database commit failed: {e}")
                return jsonify({"error": "Failed to save user in the database"}), 500

            return jsonify({
                "message": "User info successfully fetched and stored.",
                "email": email,
                "name": name,
                "jwt_access_token": jwt_access_token,
                "refresh_token": refresh_token,
                "expires_in": expires_in,
                "scope": scope
            })
        else:
            logging.error("Failed to fetch user info.")
            return jsonify({"error": "Failed to fetch user info"}), 400
    else:
        logging.error(f"Failed to obtain access token: {response.json()}")
        return jsonify({
            "error": "Failed to obtain access token",
            "details": response.json()
        }), 400
