from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.Services.delivery_service import DeliveryService


delivery_controller = Blueprint("delivery_controller", __name__)
delivery_service = DeliveryService()

# ------------------------------- View Assigned Orders -------------------------------
@delivery_controller.route("user/delivery/orders", methods=["GET"])
@jwt_required()
def view_assigned_orders():
    """
    View all orders assigned to the delivery user
    """
    try:
        delivery_email = get_jwt_identity()
        orders = delivery_service.view_assigned_orders(delivery_email)
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": f"(delivery controller) error fetching assigned orders: {str(e)}"}), 500

# ------------------------------- Change Order Status -------------------------------
@delivery_controller.route("/delivery/orders/change_status", methods=["POST"])
@jwt_required()
def change_order_status(order_id):
    """
    Change the status of an assigned order ("on_the_way","delivered")
    """
    try:
        delivery_email = get_jwt_identity()
        data = request.get_json()
        orderId = data.get("order_id")
        new_status = data.get("status")
        result = delivery_service.change_order_status(orderId, delivery_email, new_status)
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"(delivery controller) Error changing order status: {str(e)}"}), 500


