from flask import request, jsonify
from app.services.order_service import fetch_orders_for_customer

# ------------------------- Get My Orders -------------------------
def my_orders():
    try:
        customeremail = request.args.get('customeremail')
        if not customeremail:
            return jsonify({"error": "Customer email is required"}), 400

        # Fetch orders from the service
        orders = fetch_orders_for_customer(customeremail)

        if not orders:
            return jsonify({"message": "No orders found for this customer"}), 404

        return jsonify(orders), 200
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({"error": "Internal server error"}), 500
