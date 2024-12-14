from flask import Blueprint, jsonify, request
from app.Services.auth_service import AuthService
from flask_jwt_extended import jwt_required
from app.Middlewares.auth_middleware import token_required

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


'''=================================== Users | Forget Password ====================================''' 

@auth_controller.route("/App/User/ForgetPassword", methods=["PUT"]) 
def forget_password():
    data = request.get_json()
    response, status_code = auth_service.new_password(data)
    return jsonify(response), status_code
# -------------------------------------------------------------------------------

'''=================================== Test auth middleware ====================================''' 

@auth_controller.route("/App/User/profile", methods=["GET"]) 
@token_required(roles=['admin','customer'])
def get_profile():
    return jsonify({'message': f"Welcome {request.user}, your role is {request.role}"})

