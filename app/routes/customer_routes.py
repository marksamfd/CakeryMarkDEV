from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.customer_service import (get_all_products,get_product_details)  

customer_routes = Blueprint('customer_routes', __name__)

# all products for "Shop" page
@customer_routes.route('/customer/shop', methods=['GET'])
# @jwt_required()  
def shop():
    # a list of all products
    products = get_all_products()
    return jsonify(products), 200

# get the product details
@customer_routes.route('/Product/<int:product_id>', methods=['GET'])
# @jwt_required()
def product_details(product_id):
    # Fetch product details based on product_id
    product = get_product_details(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404
