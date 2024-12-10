from flask import Blueprint, jsonify
from app.Services.customer_service import CustomerService

customer_controller = Blueprint("customer_controller", __name__)

@customer_controller.route("/customer/shop", methods=["GET"])
def shop():
    service = CustomerService()
    products = service.get_all_products()
    return jsonify(products), 200
