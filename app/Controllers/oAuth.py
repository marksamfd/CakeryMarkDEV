from flask import Blueprint, redirect, request, jsonify
import os
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
SCOPE = os.getenv("SCOPE")

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
    It exchanges the authorization code for an access token and refresh token. 
    """
    # Retrieve the authorization code from the query parameters
    auth_code = request.args.get('code')

    # If the authorization code is missing, log an error and return an error response
    if not auth_code:
        logging.error("Authorization code not found in callback request.")
        return jsonify({"error": "Authorization code not found"}), 400

    # Log the received authorization code for debugging purposes
    logging.debug(f"Received authorization code: {auth_code}")

    # Google token URL used to exchange the authorization code for access tokens
    token_url = 'https://oauth2.googleapis.com/token'

    # Prepare the payload to exchange the authorization code for access and refresh tokens
    payload = {
        'code': auth_code,  # The authorization code returned by Google
        'client_id': CLIENT_ID,  
        'client_secret': CLIENT_SECRET,  
        'redirect_uri': REDIRECT_URI,  
        'grant_type': 'authorization_code'  # The grant type indicating it's an authorization code exchange
    }

    # Send a POST request to Google to exchange the authorization code for tokens
    response = requests.post(token_url, data=payload)

    # Check if the token exchange was successful (HTTP 200)
    if response.status_code == 200:
        # Parse the JSON response to extract the tokens
        token_data = response.json()
        logging.info("Successfully obtained access token.")

        # Return the token data (access token, refresh token)
        return jsonify(token_data)
    else:
        # If the token exchange fails, log the error and return a failure response
        logging.error(f"Failed to obtain access token: {response.json()}")
        return jsonify({
            "error": "Failed to obtain access token",
            "details": response.json()  # Show error details in the response
        }), 400
