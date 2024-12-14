from flask import Blueprint, request, jsonify
from app.Services.admin_service import AdminService
from app.Services.order_service import OrderService
from flask_jwt_extended import jwt_required

admin_controller = Blueprint("admin_controller", __name__)

order_service = OrderService()
admin_service = AdminService()


@admin_controller.route("/App/User/Admin/ViewCustomers", methods=["GET"]) # -- checked
@jwt_required()
def view_customers():
    """
    View all customers
    """
    customers = admin_service.get_customers()
    return jsonify(customers), 200


@admin_controller.route("/App/User/Admin/ViewStaff", methods=["GET"]) # -- checked
@jwt_required()
def view_staff():
    """
    View all staff users
    """
    staff = admin_service.get_users()
    return jsonify(staff), 200


@admin_controller.route("/App/User/Admin/AddStaff", methods=["POST"])
@jwt_required()
def add_staff():   
    try: 
        data = request.get_json()
        response = admin_service.add_user(data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f" (route) can't add a staff user: {e}"}), 500
    


@admin_controller.route("/App/User/Admin/DeleteStaff", methods=["DELETE"])
@jwt_required()
def delete_staff():
    data = request.get_json()
    response, status_code = admin_service.delete_user(data)
    return jsonify(response), status_code

@admin_controller.route("/App/User/Admin/products", methods=["GET"])
@jwt_required()
def view_products():
    """
    View all products ( raw materials and products )
    """
    products = admin_service.get_products()
    return jsonify(products), 200

@admin_controller.route("/App/User/Admin/EditPrices", methods=["PUT"])
@jwt_required()
def edit_products():
    """
    Edit product and raw material prices
    """
    data = request.get_json()
    response, status_code = admin_service.edit_product(data)
    return jsonify(response), status_code

@admin_controller.route("/App/User/Admin/AddVoucher", methods=["POST"])
@jwt_required()
def add_voucher():
    data = request.get_json()
    response, status_code = admin_service.add_voucher(data)
    return jsonify(response), status_code

@admin_controller.route("/App/User/Admin/EditVoucher", methods=["PUT"])
@jwt_required()
def edit_voucher():
    data = request.get_json()
    response, status_code = admin_service.edit_vocher(data)
    return jsonify(response), status_code

@admin_controller.route("/App/User/Admin/DeleteVoucher", methods=["DELETE"])
@jwt_required()
def delete_voucher():
    data = request.get_json()
    response, status_code = admin_service.delete_voucher(data)
    return jsonify(response), status_code
