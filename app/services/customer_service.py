from app.db import db
from sqlalchemy.sql import text

def get_all_products():
    # all products from the Inventory table
    query = text("SELECT ProductID, Name, Price FROM Inventory")
    results = db.session.execute(query).mappings().all()  # 
    # debug statement
    print(results)
    return [dict(row) for row in results]

def get_product_details(product_id):
    # get all details of a product based on product_id
    query = text("SELECT * FROM Inventory WHERE ProductID = :product_id")
    result = db.session.execute(query, {"product_id": product_id}).mappings().first()  # Use mappings() and first()
    return dict(result) if result else None
