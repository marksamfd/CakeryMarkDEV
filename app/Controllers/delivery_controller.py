from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

delivery_controller = Blueprint("delivery_controller", __name__) 

# ------------------------------- View Assigned Orders -------------------------------
@delivery_controller.route("/cakery/user/delivery/orders", methods=["GET"])
@jwt_required()
def view_assigned_orders():
    """
    View all orders assigned to the delivery user
    """
    try:
        delivery_email = get_jwt_identity()
        delivery_service = delivery_controller.delivery_service  #  injected delivery service
        orders = delivery_service.view_assigned_orders(delivery_email)
        return jsonify(orders, f"orders of {delivery_email}"), 200
    except Exception as e:
        return jsonify({"error": f"(delivery controller) error fetching assigned orders: {str(e)}"}), 500

# ------------------------------- Change Order Status -------------------------------
@delivery_controller.route("/cakery/user/delivery/orders/change_status", methods=["POST"])
@jwt_required()
def change_order_status():
    """
    Change the status of an assigned order ("out_for_delivery","delivered").
    """
    try:
        delivery_email = get_jwt_identity()
        delivery_service = delivery_controller.delivery_service  #  injected delivery service
        data = request.get_json()
        order_id = data.get("order_id")
        new_status = data.get("status")

        # -------- check if the order is assigned to the delivery user --------
        assigned_orders = delivery_service.view_assigned_orders(delivery_email)
        assigned_order_ids = [order["orderID"] for order in assigned_orders]
        if order_id not in assigned_order_ids:
            return jsonify({"error": "This order isn't assigned to this delivery user"}), 403
        # ---------------------------------

        # Change the order status
        result = delivery_service.mark_order_status(order_id, new_status)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"(delivery controller) Error changing order status: {str(e)}"}), 500

    '''=================================== Get Deliveryman Name ===================================='''
@delivery_controller.route("/cakery/user/delivery/name", methods=["GET"])
@jwt_required() 
def get_deliveryman_name():
    delivery_email = get_jwt_identity()
    delivery_service = delivery_controller.delivery_service
    name = delivery_service.get_deliveryman_name(delivery_email)
    return jsonify(name), 200
