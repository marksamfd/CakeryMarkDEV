from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.Services.delivery_service import DeliveryService
from app.Services.order_service import OrderService


delivery_controller = Blueprint("delivery_controller", __name__)
delivery_service = DeliveryService()
order_service = OrderService()

# ------------------------------- View Assigned Orders -------------------------------
@delivery_controller.route("/user/delivery/orders", methods=["GET"])
@jwt_required()
def view_assigned_orders():
    """
    View all orders assigned to the delivery user
    """
    try:
        delivery_email = get_jwt_identity()
        orders = delivery_service.view_assigned_orders(delivery_email)
        return jsonify(orders,f"orders of {delivery_email}"), 200
    except Exception as e:
        return jsonify({"error": f"(delivery controller) error fetching assigned orders: {str(e)}"}), 500

# ------------------------------- Change Order Status -------------------------------
@delivery_controller.route("/user/delivery/orders/change_status", methods=["POST"])
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
        # -------- check if the order is assigned to the delivery user --------
        assigned_orders = DeliveryService().view_assigned_orders(delivery_email)
        assigned_order_ids = [order["orderID"] for order in assigned_orders]

        if order_id not in assigned_order_ids:
            return jsonify({"error": "This order isn't assigned to this delivery user"}), 403
        # ---------------------------------

    
        result = order_service.update_order_status(orderId, new_status) # change the order status from the order service/repo 
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    

    except Exception as e:
        return jsonify({"error": f"(delivery controller) Error changing order status: {str(e)}"}), 500


