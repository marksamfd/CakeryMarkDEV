from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.Middlewares.auth_middleware import token_required
delivery_controller = Blueprint("delivery_controller", __name__)


# ------------------------------- View Assigned Orders -------------------
@delivery_controller.route("/cakery/user/delivery/orders", methods=["GET"])
@token_required(roles=['delivery'])
def view_assigned_orders():
    """
    View All Assigned Orders
    ---
    tags:
      - Delivery
    summary: Retrieve all orders assigned to the authenticated delivery user
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of orders assigned to the delivery user
        schema:
          type: object
          properties:
            orders:
              type: array
              items:
                type: object
                properties:
                  customerName:
                    type: string
                    example: "Jane Smith"
                  phone:
                    type: string
                    example: "+1234567890"
                  location:
                    type: string
                    example: "https://maps.google.com/?q=456+Elm+St"
                  numberOfItems:
                    type: integer
                    example: 3
                  status:
                    type: string
                    example: "preparing"
                  price:
                    type: number
                    format: float
                    example: 75.00
            message:
              type: string
              example: "Orders of delivery_user@example.com retrieved successfully."
      403:
        description: Forbidden - User does not have access to these orders
        schema:
          type: object
          properties:
            error:
              type: string
              example: "This user does not have access to these orders."
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "(delivery controller) error fetching assigned orders: Detailed error message."
    """
    try:
        delivery_email = request.user
        delivery_service = (
            delivery_controller.delivery_service
        )  # Injected delivery service
        orders = delivery_service.view_assigned_orders(delivery_email)
        return (
            jsonify(
                {
                    "orders": orders,
                    "message": f"Orders of {delivery_email} retrieved successfully.",
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": f"(delivery controller) error fetching assigned orders: {str(e)}"
                }
            ),
            500,
        )


# ------------------------------- Change Order Status --------------------
@delivery_controller.route(
    "/cakery/user/delivery/orders/change_status", methods=["POST"]
)
@token_required(roles=['delivery'])
def change_order_status():
    """
    Change Order Status
    ---
    tags:
      - Delivery
    summary: Update the status of an assigned order to "out_for_delivery" or "delivered"
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Details for changing the order status
        required: true
        schema:
          type: object
          required:
            - order_id
            - status
          properties:
            order_id:
              type: integer
              example: 401
            status:
              type: string
              enum: ["out_for_delivery", "delivered"]
              example: "out_for_delivery"
    responses:
      200:
        description: Order status updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order status updated successfully"
      400:
        description: Bad Request - Missing order ID, invalid status, or other validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid status provided."
      403:
        description: Forbidden - Order not assigned to this delivery user
        schema:
          type: object
          properties:
            error:
              type: string
              example: "This order isn't assigned to this delivery user."
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "(delivery controller) Error changing order status: Detailed error message."
    """
    try:
        delivery_email = request.user
        delivery_service = delivery_controller.delivery_service  # Injected delivery service
        data = request.get_json()

        # Validate payload
        if not data:
            return jsonify({"error": "Request payload is missing or not JSON"}), 400

        # Extract order_id and status
        order_id = data.get("order_id")
        new_status = data.get("status")

        if not order_id or not new_status:
            return jsonify({"error": "Order ID and status are required"}), 400

        # Check if the order is assigned to the delivery user
        assigned_orders = delivery_service.view_assigned_orders(delivery_email)
        print(f"Assigned Orders: {assigned_orders}")

        assigned_order_ids = [order.get("order_id") for order in assigned_orders if "order_id" in order]

        if order_id not in assigned_order_ids:
            return jsonify({"error": "This order isn't assigned to this delivery user."}), 403

        # Change the order status
        result = delivery_service.mark_order_status(order_id, new_status)
        if isinstance(result, dict) and "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Order status updated successfully."}), 200

    except Exception as e:
        return jsonify({"error": f"(delivery controller) Error changing order status: {str(e)}"}), 500


    # ------------------------------- Get Deliveryman Name -------------------
@delivery_controller.route("/cakery/user/delivery/name", methods=["GET"])
@token_required(roles=['delivery'])
def get_deliveryman_name():
    """
    Get Deliveryman's Name
    ---
    tags:
      - Delivery
    summary: Retrieve the authenticated delivery user's full name
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: The delivery user's full name
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Alex Johnson"
      404:
        description: Delivery user not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Delivery user not found."
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "(delivery controller) can't get deliveryman name: Detailed error message."
    """
    try:
        delivery_email = request.user
        delivery_service = delivery_controller.delivery_service
        name = delivery_service.get_deliveryman_name(delivery_email)
        if not name:
            return jsonify({"error": "Delivery user not found."}), 404
        return jsonify({"name": name}), 200
    except Exception as e:
        return (
            jsonify(
                {"error": f"(delivery controller) can't get deliveryman name: {str(e)}"}
            ),
            500,
        )
