from flask import request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps


# Middleware for token authentication
def token_required(roles=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                # Verify the JWT and retrieve claims
                verify_jwt_in_request()
                claims = get_jwt()

                # Check if the user's role matches the allowed roles (if
                # specified)
                if roles and claims.get("role") not in roles:
                    return jsonify({"message": "Permission denied!"}), 403

                # Attach user info to the request
                request.user = claims.get(
                    "sub"
                )  # 'sub' typically holds the identity (email)
                request.role = claims.get("role")
            except Exception as e:
                return jsonify({"message": str(e)}), 401

            return f(*args, **kwargs)

        return decorated

    return wrapper
