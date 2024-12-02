from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# env
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # database configuration (have to be moved to .env file)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask Secret Key
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Load SECRET_KEY from .env

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # load the jwt secret key from .env
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Look for JWTs in headers
    app.config['JWT_HEADER_NAME'] = 'Authorization'  
    app.config['JWT_HEADER_TYPE'] = 'Bearer'         
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Disable expiration for testing.

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        try:
            # Test database connection
            db.session.execute(text("SELECT 1"))
            print("Database connection successful!")
        except Exception as e:
            print("connection failed")
            print(f"Error: {e}")

    # Optional Debugging/Testing Code (Comment out in production)
    '''
    # Query to fetch all rows from CustomerUser table
    try:
        results = db.session.execute(
            text(
                """
                SELECT customeremail, password, firstname, lastname, phonenum, addressgooglemapurl, createdat
                FROM public.customeruser
                """
            )
        )
        results = results.mappings().all()  # Enable column key mapping

        if results:
            print("All rows in CustomerUser table:")
            for row in results:
                print(dict(row))  # Convert each mapping to a dictionary
        else:
            print("CustomerUser table is empty.")
    except Exception as e:
        print(f"Error querying CustomerUser table: {e}")
    '''
