from flask import Blueprint, redirect, request, jsonify
import os
from app.models import CustomerUser
from app.db import db
from datetime import datetime
from flask_jwt_extended import create_access_token
import logging
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests

# Load environment variables
load_dotenv()

# Logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Google OAuth credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

# OAuth Blueprint
google_oauth = Blueprint("google_oauth", __name__)

@google_oauth.route("/App/User/Google-Signin", methods=["GET"])
def google_signin():
    """
    Initiate Google OAuth Flow for Sign-In
    ---
    tags:
      - User
    summary: Redirects the user to Google's OAuth consent screen to authenticate and authorize the application.
    description: This endpoint redirects the user to Google's OAuth consent screen where they will be prompted to grant the application access to their Google profile and email.
    responses:
      302:
        description: Redirects the user to Google's OAuth consent screen
        headers:
          Location:
            description: The URL of the OAuth consent screen.
            schema:
              type: string
              example: "https://accounts.google.com/o/oauth2/v2/auth?client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=SCOPE&response_type=code&access_type=offline"
    """
    # Construct the Google OAuth URL with necessary parameters
    google_oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={SCOPE}&"
        f"response_type=code&"
        f"access_type=offline"
    )

    # Log the URL for debugging purposes
    logging.debug(f"Redirecting to Google OAuth URL: {google_oauth_url}")

    # Redirect the user to the Google OAuth URL to begin the sign-in process
    return redirect(google_oauth_url)


@google_oauth.route("/App/User/Google-Callback", methods=["POST"])
def google_callback():
    """
    Handle Google OAuth Callback and Exchange Authorization Code for Access Token
    ---
    tags:
      - User
    summary: Handles the callback from Google after the user authorizes the application. It exchanges the authorization code for an access token and stores or retrieves the user's data.
    description: This endpoint handles the callback from Google after the user logs in. It exchanges the authorization code for an access token, verifies the user's identity, and either creates a new user or returns an existing user’s JWT access token.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              code:
                type: string
                description: The authorization code returned by Google after user login.
                example: "4/0AX4XfWhbmZPn5e95_aBPTwFk8vLeXyl4ixpkeKjiw_cHk77rFGhZDqwr0XpxK2eaf4DzF4"
    responses:
      200:
        description: User already exists, and JWT access token is returned
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User already exists with this email"
                status:
                  type: string
                  example: "error"
                jwt_access_token:
                  type: string
                  example: "jwt_token_here"
      400:
        description: Authorization code not found or invalid email format
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Authorization code not found"
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Failed to save user in the database"
    security:
      - BearerAuth: []
    """
    auth_code = request.get_json().get("code")

    if not auth_code:
        logging.error("Authorization code not found in callback request.")
        return jsonify({"error": "Authorization code not found"}), 400

    # Verify the ID token and extract user information
    idinfo = id_token.verify_oauth2_token(auth_code, requests.Request(), CLIENT_ID)
    email = idinfo.get("email")
    
    # Extract domain
    domain = email.split("@")[1] if "@" in email else None
    if not domain:
        return (
            jsonify({"message": "Invalid email format", "status": "error"}),
            400,
        )

    # Create JWT token for the user
    additional_claims = {"role": "customer"}
    jwt_access_token = create_access_token(
        identity=email, additional_claims=additional_claims
    )

    # Check if the user already exists
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

    # Add new user to the database
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
            "name": f"{firstname} {lastname}",
            "jwt_access_token": jwt_access_token,
        }
    )
