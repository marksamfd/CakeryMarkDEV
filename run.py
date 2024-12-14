from app.db import create_app, db
from app.Controllers.customer_controller import customer_controller
from app.Controllers.baker_controller import baker_controller
from app.Controllers.auth_controller import auth_controller
from app.Controllers.delivery_controller import delivery_controller
from app.Controllers.admin_controller import admin_controller
from app.Middlewares.error_middleware import error_middleware
from flask_jwt_extended import JWTManager


app = create_app()
jwt = JWTManager(app)
error_middleware(app)
app.register_blueprint(customer_controller)
app.register_blueprint(baker_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(delivery_controller)
app.register_blueprint(admin_controller)


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
