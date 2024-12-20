from flask import Blueprint, jsonify, request
from app.Services.baker_service import BakerService
from flask_jwt_extended import jwt_required
from app.Middlewares.auth_middleware import token_required

baker_controller = Blueprint("baker_controller", __name__)
baker_service = BakerService()

"""=================================== Baker | Orders ===================================="""  # - checked


@baker_controller.route("/cakery/user/baker/Orders", methods=["GET"])
@token_required(roles=['baker'])
def get_baker_orders():
    """
    Get All Baker Orders
    ---
    tags:
      - Baker
    summary: Retrieve all orders assigned to the baker
    security:
      - BearerAuth: []
    produces:
      - application/json
    responses:
      200:
        description: A list of baker's orders
        schema:
          type: array
          items:
            type: object
            properties:
              orderID:
                type: integer
                example: 101
              orderDate:
                type: string
                format: date-time
                example: "2024-04-25T14:30:00Z"
              customer:
                type: object
                properties:
                  email:
                    type: string
                    example: customer@example.com
              totalPrice:
                type: number
                format: float
                example: 150.75
              status:
                type: string
                example: "Pending"
      401:
        description: Unauthorized - Missing or invalid JWT token
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    orders = baker_service.view_baker_orders()
    return jsonify(orders), 200


# -------------------------------------------------------------------------------

"""=================================== Baker | Order Details ===================================="""  # - checked


@baker_controller.route(
    "/cakery/user/baker/Orders/<int:order_id>/details", methods=["GET"]
)
@token_required(roles=['baker'])
def get_order_details(order_id):
    """
    Get Specific Order Details
    ---
    tags:
      - Baker
    summary: Retrieve details of a specific order by its ID
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: The ID of the order to retrieve details for
        example: 101
    produces:
      - application/json
    responses:
      200:
        description: Detailed information of the specified order
        schema:
          type: object
          properties:
            orderID:
              type: integer
              example: 101
            orderDate:
              type: string
              format: date-time
              example: "2024-04-25T14:30:00Z"
            status:
              type: string
              example: "Pending"
            items:
              type: array
              items:
                type: object
                properties:
                  productID:
                    type: integer
                    example: 501
                  productName:
                    type: string
                    example: "Chocolate Cake"
                  quantity:
                    type: integer
                    example: 2
                  priceAtOrder:
                    type: number
                    format: float
                    example: 25.50
      404:
        description: Order not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Order not found"
      401:
        description: Unauthorized - Missing or invalid JWT token
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
    """
    order_details = baker_service.view_specific_order(order_id)
    if "error" in order_details:
        return jsonify(order_details), 404
    return jsonify(order_details), 200


# ----------------------------------------------------------------------------------

"""=================================== Baker | Update Order Status ===================================="""


@baker_controller.route(
    "/cakery/user/baker/Orders/Update_status", methods=["POST"]
)  # - checked (changing DB too)
@token_required(roles=['baker'])
def update_order_status():
    """
    Update Order Status to Prepared
    ---
    tags:
      - Baker
    summary: Mark an order as prepared and assign a delivery user
    security:
      - BearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Order status update details
        required: true
        schema:
          type: object
          required:
            - order_id
          properties:
            order_id:
              type: integer
              example: 101
    responses:
      200:
        description: Order status updated successfully and delivery assigned
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order status updated to Prepared"
            delivery_assignment:
              type: object
              properties:
                delivery_user:
                  type: string
                  example: "delivery_user@example.com"
                assigned_at:
                  type: string
                  format: date-time
                  example: "2024-04-25T15:00:00Z"
      400:
        description: Bad Request - Missing order ID or other validation errors
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Order ID and status are required"
      401:
        description: Unauthorized - Missing or invalid JWT token
        schema:
          type: object
          properties:
            msg:
              type: string
              example: "Missing Authorization Header"
      404:
        description: Order not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Order not found"
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "(repo) error updating order status: Detailed error message"
    """
    data = request.get_json()
    order_id = data.get("order_id")
    # status = data.get("status")

    if not order_id:
        return jsonify({"error": "Order ID and status are required"}), 400

    result = baker_service.mark_order_prepared(order_id)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200


# ----------------------------------------------------------------------------------
