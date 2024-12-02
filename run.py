from app.db import create_app, db  # Import the create_app function and db instance
from app.routes.customer_routes import customer_routes  # import from the routes_file, this only customer as start
from app.routes.baker_routes import baker_routes
from app.Authentication import auth_routes
from app.oAuth import google_oauth
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import *  # all models from the models file

''' 
This file will run to make the flask app run, 
it will create the app, register the blueprint, create the table in the database, 
so add other blueprints here when ant to test 
'''
from flask_cors import CORS



app = create_app()


CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}}, supports_credentials=True)
# Register the customer_routes blueprint
app.register_blueprint(customer_routes)
app.register_blueprint(baker_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(google_oauth)

with app.app_context():
    db.create_all()  # Create the table in the database

if __name__ == "__main__":
    app.run(debug=True)
