from flask import Blueprint, jsonify, request
from app.Services.auth_service import AuthService
from flask_jwt_extended import jwt_required

auth_controller = Blueprint("auth_controller", __name__)
auth_service = AuthService()

@auth_controller.route("/App/User/SignUp/<customer_email>", methods=["POST"]) 
def signup(customer_email):
    data = request.get_json()
    response, status_code = auth_service.add_new_user(customer_email, data)
    return jsonify(response), status_code

@auth_controller.route("/App/User/SignIn/<customer_email>", methods=["POST"]) 
def signin(customer_email):
    data = request.get_json()
    response, status_code = auth_service.sign_user_in(customer_email, data)
    return jsonify(response), status_code