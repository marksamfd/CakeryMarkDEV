from flask import Blueprint, jsonify, request
from app.Services.auth_service import AuthService
from flask_jwt_extended import jwt_required

auth_controller = Blueprint("auth_controller", __name__)
auth_service = AuthService()

'''=================================== Customer | SignUp ====================================''' 

@auth_controller.route("/App/User/SignUp", methods=["POST"]) 
def signup():
    data = request.get_json()
    response, status_code = auth_service.add_new_user(data)
    return jsonify(response), status_code

# -------------------------------------------------------------------------------

'''=================================== Users | SignIn ====================================''' 

@auth_controller.route("/App/User/SignIn", methods=["POST"]) 
def signin():
    data = request.get_json()
    response, status_code = auth_service.sign_user_in(data)
    return jsonify(response), status_code
# -------------------------------------------------------------------------------
