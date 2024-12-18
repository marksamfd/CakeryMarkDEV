from flask import jsonify
import logging

# Setup logging for error tracking (optional)
logging.basicConfig(level=logging.ERROR)


# Middleware to handle all errors globally
def error_middleware(app):
    @app.errorhandler(Exception)
    def handle_error(e):
        # Log the error for debugging purposes (optional)
        logging.error(f"An error occurred: {str(e)}")

        # If the error is an instance of a specific error type, return a custom
        # message
        if isinstance(e, KeyError):
            return jsonify({"message": "Missing required key"}), 400
        elif isinstance(e, ValueError):
            return jsonify({"message": "Invalid value"}), 400
        elif isinstance(e, TypeError):
            return jsonify({"message": "Type error occurred"}), 400
        else:
            # For unhandled exceptions, return a generic message
            return jsonify({"message": "An unexpected error occurred"}), 500
