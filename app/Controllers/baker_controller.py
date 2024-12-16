from flask import Blueprint, jsonify, request
from app.Services.baker_service import BakerService
from flask_jwt_extended import jwt_required

baker_controller = Blueprint("baker_controller", __name__)
baker_service = BakerService()

'''=================================== Baker | orders ===================================='''  # - checked
@baker_controller.route("/cakery/user/baker/Orders", methods=["GET"]) 
def get_baker_orders():
    orders = baker_service.view_baker_orders()
    return jsonify(orders), 200
# -------------------------------------------------------------------------------

'''=================================== Baker | order details ===================================='''  # - checked
@baker_controller.route("/cakery/user/baker/Orders/<int:order_id>/details", methods=["GET"])
def get_order_details(order_id):
    order_details = baker_service.view_specific_order(order_id)
    if "error" in order_details:
        return jsonify(order_details), 404
    return jsonify(order_details), 200
# ----------------------------------------------------------------------------------

'''=================================== Baker | update order status ===================================='''
@baker_controller.route("/cakery/user/baker/Orders/Update_status", methods=["POST"]) # - checked (changing DB too)
def update_order_status():
    data = request.get_json()
    order_id = data.get("order_id")
    # status = data.get("status")

    if not order_id:
        return jsonify({"error": "Order ID and status are required"}),400

    result = baker_service.mark_order_prepared(order_id)
    if "error" in result:
        return jsonify(result),400
    return jsonify(result),200
# ----------------------------------------------------------------------------------