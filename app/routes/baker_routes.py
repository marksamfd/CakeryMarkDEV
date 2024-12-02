from flask import Blueprint, request, jsonify
from app.services.baker_service import (get_baker_orders,get_order_details, update_order_status)
from flask_jwt_extended import jwt_required
baker_routes = Blueprint("baker_routes", __name__)


'''=================================== Baker HomePage ===================================='''
# ------------------------------------------ All orders to be baked ------------------------------------------

@baker_routes.route("/user/baker/orders", methods=["GET"])
@jwt_required()
def baker_dashboard():
    try:
        orders = get_baker_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching orders: {e}"}), 500


'''=================================== Baker | View order ===================================='''
# -------------------------------- Get details of a specific order --------------------------------

@baker_routes.route("/user/baker/orders/<int:orderID>/details", methods=["GET"])
@jwt_required()
def order_details(orderID):
    try:
        order_details = get_order_details(orderID)
        if order_details:
            return jsonify(order_details), 200
        return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching order details: {e}"}), 500


'''=================================== Baker | View order ===================================='''
# -------------------------------- Update order status & assign delivery man  --------------------------------

@baker_routes.route("/user/baker/orders/update_status", methods=["POST"])
@jwt_required()
def update_order_status_route():
    try:
        data = request.get_json()
        order_id = data.get("order_id")
        preparation_status = data.get("preparation_status")
        if not order_id or not preparation_status:
            return jsonify({"error": "input required"}), 400

        result = update_order_status(order_id, preparation_status)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error updating order: {e}"}), 500