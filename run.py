from app.db import create_app, db
from app.Controllers.customer_controller import customer_controller

app = create_app()
app.register_blueprint(customer_controller)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
