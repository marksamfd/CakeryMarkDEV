from flask import Blueprint, redirect, request, jsonify
import os
from app.models import CustomerUser, DeliveryUser, Admin, BakeryUser, Cart
from app.db import db
from datetime import datetime
from flask_jwt_extended import create_access_token
import requests
import logging
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv()

# Logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Google OAuth credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
# SCOPE = os.getenv("SCOPE")
SCOPE = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"


# OAuth Blueprint
google_oauth = Blueprint("google_oauth", __name__)


# Initiate Google Sign-In and taking permissions from user
@google_oauth.route("/App/User/Google-Signin", methods=["GET"])
def google_signin():
    """
    Redirects the user to Google's OAuth consent screen where they will
    authorize the application to access their Google profile and email.
    """
    # Construct the Google OAuth URL with necessary parameters
    google_oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"  # The redirect URI after successful login
        f"scope={SCOPE}&"  # Permissions to request from the user (email, profile, openid)
        f"response_type=code&"  # Will be exchanged with the access token
        f"access_type=offline"
    )

    # Log the URL for debugging purposes
    logging.debug(f"Redirecting to Google OAuth URL: {google_oauth_url}")

    # Redirect the user to the Google OAuth URL to begin the sign-in process
    return redirect(google_oauth_url)


# Google oAuth url for sign in
@google_oauth.route("/App/User/Google-Callback", methods=["post"])
def google_callback():
    """
    Handles the callback from Google after the user authorizes the application.
    It exchanges the authorization code for an access token and fetches the user's email.
    """
    auth_code = request.get_json().get("code")

    if not auth_code:
        logging.error("Authorization code not found in callback request.")
        return jsonify({"error": "Authorization code not found"}), 400

    # logging.debug(f"Received authorization code: {auth_code}")

    idinfo = id_token.verify_oauth2_token(auth_code, requests.Request(), CLIENT_ID)
    email = idinfo.get("email")
    # Extract domain
    domain = email.split("@")[1] if "@" in email else None
    if not domain:
        return (
            jsonify({"message": "Invalid email format", "status": "error"}),
            400,
        )

    # Check if user already exists
    additional_claims = {"role": "customer"}
    jwt_access_token = create_access_token(
        identity=email, additional_claims=additional_claims
    )
    existing_user = CustomerUser.query.filter_by(customeremail=email).first()
    if existing_user:
        return (
            jsonify(
                {
                    "message": "User already exists with this email",
                    "status": "error",
                    "jwt_access_token": jwt_access_token,
                }
            ),
            200,
        )

    firstname = idinfo.get("given_name")
    lastname = idinfo.get("family_name")

    # Current timestamp for createdat
    createdat = datetime.utcnow()

    # Add new user to database
    new_customer = CustomerUser(
        customeremail=email,
        firstname=firstname,
        lastname=lastname,
        createdat=createdat,
    )

    try:
        db.session.add(new_customer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database commit failed: {e}")
        return jsonify({"error": "Failed to save user in the database"}), 500

    return jsonify(
        {
            "message": "User info successfully fetched and stored.",
            "email": email,
            "name": name,
            "jwt_access_token": jwt_access_token,
        }
    )