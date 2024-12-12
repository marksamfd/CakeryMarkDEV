from app.db import create_app, db
from app.Controllers.customer_controller import customer_controller
from app.Controllers.baker_controller import baker_controller
from app.Controllers.auth_controller import auth_controller

app = create_app()
app.register_blueprint(customer_controller)
app.register_blueprint(baker_controller)
app.register_blueprint(auth_controller)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
