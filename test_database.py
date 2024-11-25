from app.db import create_app, db
from app.models import Inventory

''' Testing api to insure that the database is working correctly '''


def test_inventory():
   
    app = create_app()
    with app.app_context():
        try:
            items = Inventory.query.all()  # Retrieve all items
            print("items retreived") 
            for item in items:
                print(item.as_dict())  # Use the as_dict method to print each item as a dictionary
        except Exception as e:
            print("error from inventory retr")
            print(f"Error: {e}")

if __name__ == "__main__":
    test_inventory()
