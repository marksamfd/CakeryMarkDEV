from app.db import create_app, db  # Import the create_app function and db instance
from app.routes.customer_routes import customer_routes  # import from the routes_file


app = create_app()
# register the customer_routes blueprint
app.register_blueprint(customer_routes)
with app.app_context():
    db.create_all()  # create the table in the database

if __name__ == "__main__":
    app.run(debug=True)
