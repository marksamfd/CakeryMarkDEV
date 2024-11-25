from  app.models import Inventory
from sqlalchemy.sql import text

def get_all_products():
    try: 
        # all products from the Inventory table
        products = Inventory.query.all()
        return [product.as_dict() for product in products] # return a list of dictionaries, each is data of a product

    except Exception as e:
        print("all products error")
        print(f"Error: {e}")
        return None
    
def get_product_details(product_id):
    try: 
        # get all details of a product based on product_id
        product = Inventory.query.get(product_id)   # Use mappings() and first()
        return product.as_dict() if product else None  
    except Exception as e:
        print("product details error")
        print(f"Error: {e}")
        return None