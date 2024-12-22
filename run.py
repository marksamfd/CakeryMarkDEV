from app.db import create_app, db
from app.Controllers.customer_controller import customer_controller
from app.Controllers.oAuth import google_oauth
from app.Controllers.baker_controller import baker_controller
from app.Controllers.auth_controller import auth_controller
from app.Controllers.delivery_controller import delivery_controller
from app.Controllers.admin_controller import admin_controller
from app.Middlewares.error_middleware import error_middleware
from app.utils.order_status_notifier import (
    OrderStatusNotifier,
    PushNotificationObserver,
    DatabaseNotificationObserver,
)
from app.Services.otp_service import OTPService
from app.Services.delivery_service import DeliveryService
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from app.utils.order_status_notifier import FirebaseNotificationObserver

import firebase_admin
from firebase_admin import credentials

# ------- firebase initialization (push notification -------
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('cakery-b599e-firebase-adminsdk-id1z9-f98f481fc3.json')
    firebase_admin.initialize_app(cred)


swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Cakery Admin API",
        "description": "API documentation for Admin-related endpoints in Cakery",
        "version": "2.0.0",
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter 'Bearer <your JWT token>'",
        }
    },
    "produces": ["application/json"],
    "consumes": ["application/json"],
}

app = create_app()
jwt = JWTManager(app)
error_middleware(app)

# ------ Shared Dependencies ------
notifier = OrderStatusNotifier()
notifier.register_observer(PushNotificationObserver())
notifier.register_observer(DatabaseNotificationObserver())

# Initialize services with shared dependencies
otp_service = OTPService(notifier)
delivery_service = DeliveryService(notifier)

# Inject shared dependencies into controllers
delivery_controller.delivery_service = delivery_service
customer_controller.otp_service = otp_service

# Register Firebase Observer
notifier.register_observer(FirebaseNotificationObserver())

# Register Blueprints
app.register_blueprint(customer_controller)
app.register_blueprint(baker_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(delivery_controller)
app.register_blueprint(admin_controller)
app.register_blueprint(google_oauth)

# Initialize Swagger
swagger = Swagger(app, template=swagger_template)
#mkk
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
