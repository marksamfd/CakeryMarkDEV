from  app.models import Cart, CartItems, Inventory
from sqlalchemy.sql import text

from app.db import db


''' ===================================== Product Functions ===================================== '''

# ------------ Get All Products ( shop page ) ------------
def get_all_products():
    try: 
        # all products from the Inventory table
        products = Inventory.query.all()
        return [product.as_dict() for product in products] # return a list of dictionaries, each is data of a product

    except Exception as e:
        print("all products error")
        print(f"Error: {e}")
        return None


# ------------ Get Product Details ( click on product ) ------------
def get_product_details(product_id):
    try: 
        # get all details of a product based on product_id
        product = Inventory.query.get(product_id)   # Use mappings() and first()
        return product.as_dict() if product else None  
    except Exception as e:
        print("product details error")
        print(f"Error: {e}")
        return None
''' ------------------------------------------------------------------------------------------ '''

''' ===================================== Cart Functions ===================================== '''

#  ------------ Get Cart Items ------------
def get_cart_items(customeremail):
    cart = Cart.query.filter_by(customeremail=customeremail).first()
    if not cart:
        return {"error": "Cart not found"}
    return [item.as_dict() for item in cart.cart_items]



# ------------------------------- Add to Cart ------------------------------
def add_to_cart(customeremail, product_id, quantity):
    '''
    Add a product to the cart and if the product already exists in the cart, 
    increments the quantity, If not it will add ot as new item to the cart.
    '''
    # customer cart
    cart = Cart.query.filter_by(customeremail=customeremail).first()
    if not cart:
        return {"error": f"Cart not found for {customeremail}"}

    # Check if the product exists in the inventory
    try:
        product = Inventory.query.get(product_id)
        if not product:
            return {"error": f"Product with ID {product_id} not found in database"}
    except Exception as e:
        print(f"Error fetching product from database: {e}")
        return {"error": "Database error while fetching product"}

    # Check if the product is already in the cart
    try:
        cart_item = CartItems.query.filter_by(cartid=cart.cartid, productid=product_id).first()
        if cart_item:
            # increment quantity if it's already in the cart
            cart_item.quantity += quantity
        else:
            # new item
            cart_item = CartItems(cartid=cart.cartid, productid=product_id, quantity=quantity, price=product.price)
            db.session.add(cart_item)

        # save to DB
        db.session.commit()
        return {"message": f"Product {'updated' if cart_item else 'added'} to cart"}
    except Exception as e:
        print(f"Error: {e}")
        print("Error during the addition or update process in add_to_cart")
        return {"error": "Error adding product to cart"}




# -------------------------------------- Remove from Cart --------------------------------------
def remove_from_cart(customeremail, product_id):

    ''' Removes a product completely from  cart '''


    # cart retrival 
    cart = Cart.query.filter_by(customeremail=customeremail).first()
    if not cart:
        return {"error": f"Cart not found for {customeremail}"}

    try: # check if it's in inventory
        cart_item = CartItems.query.filter_by(cartid=cart.cartid, productid=product_id).first()
        if not cart_item:
            return {"error": f"Product with ID {product_id} not found in cart"}

        # remove item from the cart
        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Product removed from cart"}
    except Exception as e:
        print(f"Error: {e}")
        print("Error during the deletion process in remove_from_cart")
        return {"error": "Error removing product from cart"}


