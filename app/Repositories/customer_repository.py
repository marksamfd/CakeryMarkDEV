from app.db import db
from app.models import Inventory

class CustomerRepository:
    def get_all_products(self):
        try:
            products = Inventory.query.all()
            return [product.as_dict() for product in products]
        except Exception as e:
            print("Error fetching products:", e)
            return []
