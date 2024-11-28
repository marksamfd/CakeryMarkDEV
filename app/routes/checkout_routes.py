from flask import request, jsonify
from app.services.checkout_service import process_checkout

# ------------------------- Checkout Route -------------------------
def checkout():
    try:
        data = request.get_json()
        customeremail = data.get('customeremail')

        # Delegate checkout processing to the service layer
        result = process_checkout(customeremail, data)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 201
    except Exception as e:
        print(f"Error in /customer/checkout: {e}")
        return jsonify({"error": "Internal server error"}), 500
