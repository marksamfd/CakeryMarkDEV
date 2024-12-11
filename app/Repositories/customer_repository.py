from app.models import Inventory, Cart, CartItems,Rawmaterials,CustomizeCake,Customize_Cake_Layers
from app.db import db


class CustomerRepository:
    # --------------------------- get all products ---------------------------
    def get_all_products(self):
        try:
            products = Inventory.query.all()
            return [product.as_dict() for product in products]
        except Exception as e:
            print(f"(repo) can't get all products: {e}")
            return []
    # --------------------------- get product by id ---------------------------
    def get_product_by_id(self, product_id):
        try:
            product = Inventory.query.get(product_id)
            return product.as_dict() if product else None
        except Exception as e:
            print(f"(repo) can't get product by id: {e}")
            return None
    # --------------------------- get cart ---------------------------
    def get_cart(self, customer_email):
        try:
            cart = Cart.query.filter_by(customeremail=customer_email).first() # get the cart of the customer 
            if not cart:
                return {"error": "Cart not found"}
            
            cart_items = [
                {
                    "productid": item.productid,
                    "quantity": item.quantity,
                    "price": item.price,
                    "productname": Inventory.query.get(item.productid).name if Inventory.query.get(item.productid) else None,
                }
                for item in cart.cart_items
            ]
            return {"cart_id": cart.cartid,"items": cart_items}
        except Exception as e:
            print(f" (repo) cant get cart: {e}")
            return {"error": "An error occurred while fetching the cart"}
        
    # --------------------------- add item to cart ---------------------------
    def add_item_to_cart(self, customer_email, product_id, quantity):
        try:
            cart = Cart.query.filter_by(customeremail=customer_email).first() # get the cart of the customer
            if not cart:
                return {"error": "(repo) cart not found for this customer"}
            
            product = Inventory.query.get(product_id)
            if not product:
                return {"error": "(repo) product not found"}

            cart_item = CartItems.query.filter_by(cartid=cart.cartid,productid=product_id).first() # check if the product is already in the cart
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItems(cartid=cart.cartid, productid=product_id, quantity=quantity, price=product.price)
                db.session.add(cart_item)

            db.session.commit()
            return {"message": f"added to cart successfully, cart id: {cart.cartid}"}
    
        except Exception as e:
            db.session.rollback()
            return {"error": "(repo) can't add item to cart: {e}"}
    # ----------------------------------------------------------------------------------------
    # --------------------------- remove item from cart ---------------------------------------
    def remove_from_cart(self, customer_email, product_id):
        try:
            # ------- get cart --------
            cart = Cart.query.filter_by(customeremail=customer_email).first()
            if not cart:
                return {"error": "(repo) Cart not found for this customer"}
            # ------ item in cart --------
            cart_item = CartItems.query.filter_by(cartid=cart.cartid,productid=product_id).first()
            if not cart_item:
                return {"error": "(repo) Item not found in the cart"}
            # ---------------------------
            db.session.delete(cart_item)
            db.session.commit()
            return {"message": "Item removed from cart successfully"}
        
        except Exception as e:
            db.session.rollback()
            return {"error": "error occurred while removing the item from the cart", "error_details": str(e)}
#
    def get_raw_materials(self):
        raw_materials = Rawmaterials.query.all()

        # Serialize raw materials into dictionaries
        serialized_data = [material.as_dict() for material in raw_materials]

        return serialized_data

    def create_custom_cake(self,customer_email, data):
        cake_shape = data.get("cakeshape")
        cake_size = data.get("cakesize")
        cake_type = data.get("caketype")
        cake_flavor = cake_type  # Assuming type is flavor
        message = data.get("message", "")
        layers = data.get("layers", [])
        num_layers = len(layers)

        # Create the parent CustomizeCake record
        new_customized_cake = CustomizeCake(
            numlayers=num_layers,
            customeremail=customer_email,
            cakeshape=cake_shape,
            cakesize=cake_size,
            cakeflavor=cake_flavor,
            message=message
        )
        db.session.add(new_customized_cake)
        db.session.commit()  # Commit to generate ID

        # Add layers
        for i, layer in enumerate(layers):
            inner_fillings = layer.get("innerFillings", "")
            inner_toppings = layer.get("innerToppings", "")
            outer_coating = layer.get("outerCoating", "")
            outer_toppings = layer.get("outerToppings", "")

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
