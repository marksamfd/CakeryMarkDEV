from  app.models import Cart, CartItems, Inventory,CustomizeCake,Customize_Cake_Layers,Rawmaterials
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from app.models import Voucher, Orders, OrderItems


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


''' ===================================== Customize Cake Functions ===================================== '''
# -------------------------------------- Add the customized cake data to the database --------------------------------------
def create_customized_cake(email, data):
    cake_shape = data.get("cakeshape")
    cake_size = data.get("cakesize")
    cake_flavor = data.get("caketype")
    message = data.get("message", "")
    layers = data.get("layers", [])
    num_layers = len(layers)

    # Create the parent CustomizeCake record
    new_customized_cake = CustomizeCake(
        numlayers=num_layers,
        customeremail=email,
        cakeshape=cake_shape,
        cakesize=cake_size,
        cakeflavor=cake_flavor,
        message=message
    )
    db.session.add(new_customized_cake)
    db.session.commit()  # Commit to generate ID

    # Add layers
    for i, layer in enumerate(layers):
        inner_fillings = layer.get("innerfillings", "")
        inner_toppings = layer.get("innertoppings", "")
        outer_coating = layer.get("outercoating", "")
        outer_toppings = layer.get("outertoppings", "")

        new_layer = Customize_Cake_Layers(
            customizecakeid=new_customized_cake.customizecakeid,
            layer=i + 1,
            innerfillings=inner_fillings,
            innertoppings=inner_toppings,
            outercoating=outer_coating,
            outertoppings=outer_toppings
        )
        db.session.add(new_layer)

    # Final commit
    db.session.commit()

    return {"message": "Cake customization created successfully!", "customizecakeid": new_customized_cake.customizecakeid}

# -------------------------------------- Send all the raw materials data --------------------------------------

def get_raw_materials():
    """
    Fetches all raw materials and their prices from the database.
    Returns a list of serialized raw material objects.
    """
    # Query all raw materials
    raw_materials = Rawmaterials.query.all()

    # Serialize raw materials into dictionaries
    serialized_data = [material.as_dict() for material in raw_materials]

    return serialized_data


'''=================================== Checkout Service ==================================='''
def process_checkout(customer_email, voucher_code=None):
    # cart of customer making his order
    cart = Cart.query.filter_by(customeremail=customer_email).first()
    if not cart or not cart.cart_items:
        return {"error": "Cart is empty or does not exist"}

    # Calculate the total price of the cart
    total_price = sum(item.quantity * item.price for item in cart.cart_items)

    # Apply voucher discount if a voucher code is provided
    if voucher_code:
        voucher = Voucher.query.filter_by(vouchercode=voucher_code).first()
        if not voucher:
            return {"error": "Invalid voucher code"}
        discount = total_price * (voucher.discountpercentage / 100)
        total_price -= discount

    try:
        # Create a new order
        new_order = Orders(
            customeremail=customer_email,
            totalprice=total_price,
            status="preparing", 
        )
        db.session.add(new_order)
        db.session.flush()  # Allows us to retrieve the order ID immediately

        # Add items from the cart to the order
        for item in cart.cart_items:
            order_item = OrderItems(
                orderid=new_order.orderid,
                productid=item.productid,
                customcakeid=item.customcakeid,
                quantity=item.quantity,
                priceatorder=item.price
            )
            db.session.add(order_item)
        # Clear the cart after successful order creation
        db.session.delete(cart)  # Delete the entire cart (or you can clear the cart items separately)
        # Commit all changes
        db.session.commit()
        return {"message": "Checkout successful", "order_id": new_order.orderid, "total_price": total_price}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Database error during checkout: {e}"}



'''=================================== My Orders Service ==================================='''
def get_customer_orders(customer_email):
    # Retrieve all orders for the customer
    orders = Orders.query.filter_by(customeremail=customer_email).all()
    if not orders:
        return {"message": "No orders found"}

    # Format orders into a list of dictionaries
    return [
        {
            "orderID": order.orderid,
            "orderDate": order.orderdate.isoformat() if order.orderdate else None,
            "status": order.status,
            "totalPrice": float(order.totalprice) if order.totalprice else 0,
            "items": [
                {
                    "productID": item.productid,
                    "quantity": item.quantity,
                    "priceAtOrder": float(item.priceatorder) if item.priceatorder else 0
                }
                for item in order.order_items
            ]
        }
        for order in orders
    ]



''' ===================================== Customize Cake Functions ===================================== '''
# -------------------------------------- Add the customized cake data to the database --------------------------------------
def create_customized_cake(email, data):
    cake_shape = data.get("cakeshape")
    cake_size = data.get("cakesize")
    cake_flavor = data.get("caketype")
    message = data.get("message", "")
    layers = data.get("layers", [])
    num_layers = len(layers)

    # Create the parent CustomizeCake record
    new_customized_cake = CustomizeCake(
        numlayers=num_layers,
        customeremail=email,
        cakeshape=cake_shape,
        cakesize=cake_size,
        cakeflavor=cake_flavor,
        message=message
    )
    db.session.add(new_customized_cake)
    db.session.commit()  # Commit to generate ID

    # Add layers
    for i, layer in enumerate(layers):
        inner_fillings = layer.get("innerfillings", "")
        inner_toppings = layer.get("innertoppings", "")
        outer_coating = layer.get("outercoating", "")
        outer_toppings = layer.get("outertoppings", "")

        new_layer = Customize_Cake_Layers(
            customizecakeid=new_customized_cake.customizecakeid,
            layer=i + 1,
            innerfillings=inner_fillings,
            innertoppings=inner_toppings,
            outercoating=outer_coating,
            outertoppings=outer_toppings
        )
        db.session.add(new_layer)

    # Final commit
    db.session.commit()

    return {"message": "Cake customization created successfully!", "customizecakeid": new_customized_cake.customizecakeid}

# -------------------------------------- Send all the raw materials data --------------------------------------

def get_raw_materials():
    """
    Fetches all raw materials and their prices from the database.
    Returns a list of serialized raw material objects.
    """
    # Query all raw materials
    raw_materials = Rawmaterials.query.all()

    # Serialize raw materials into dictionaries
    serialized_data = [material.as_dict() for material in raw_materials]

    return serialized_data