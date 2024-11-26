from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text  # all imports will be summed up further, wait till map the hiererchy of files
import secrets
from dotenv import load_dotenv
import os

''' 
connect to the database, and create the app, lower part and creation was for testing the database connection directly before model mapping
'''


load_dotenv() # load the secret key from .env file, to seperate secret code temporary, also database link is manually implemented to ease testing between us

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:aabb1122@localhost:5432/Cakery"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
            print("Database connection failed or query error!")
            print(f"Error: {e}")


# test after running with your configuration 
'''  
 # Query to fetch all rows from CustomerUser table
            results = db.session.execute(
                text(
                    """
                    SELECT customeremail, password, firstname, lastname, phonenum, addressgooglemapurl, createdat
                    FROM public.customeruser
                    """
                )
            )

            # Enable column key mapping
            results = results.mappings().all()
            
            if results:
                print("All rows in CustomerUser table:")
                for row in results:
                    print(dict(row))  # Convert each mapping to a dictionary
            else:
                print("CustomerUser table is empty.")

'''
