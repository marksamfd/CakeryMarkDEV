from app.models import (
    Inventory,
    Cart,
    CartItems,
    Rawmaterials,
    CustomizeCake,
    Customize_Cake_Layers,
    CustomerUser,
    Notification,
    Review,
)
from app.db import db
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher


ph = PasswordHasher()
load_dotenv()


class CustomerRepository:
    # ============================== get all products ========================
    def get_all_products(self):
        try:
            products = Inventory.query.all()
            return [product.as_dict() for product in products]
        except Exception as e:
            print(f"(repo) can't get all products: {e}")
            return []
    
    def hash_password(self, password):
        return ph.hash(password)

    # ==============================================================================

    # ============================== get product by id =======================
    def get_product_by_id(self, product_id):
        try:
            product = Inventory.query.get(product_id)
            return product.as_dict() if product else None
        except Exception as e:
            print(f"(repo) can't get product by id: {e}")
            return None

    # ============================== get cart ==============================
    def get_cart(self, customer_email):
        try:
            cart = Cart.query.filter_by(
                customeremail=customer_email
            ).first()  # get the cart of the customer
            if not cart:
                return {"error": "Cart not found"}

            cart_items = [
                {
                    "productid": item.productid,
                    "customcakeid": item.customcakeid,
                    "quantity": item.quantity,
                    "price": item.price,
                    "productname": (
                        Inventory.query.get(item.productid).name
                        if Inventory.query.get(item.productid)
                        else None
                    ),
                }
                for item in cart.cart_items
            ]
            return {"cart_id": cart.cartid, "items": cart_items}
        except Exception as e:
            print(f" (repo) cant get cart: {e}")
            return {"error": "An error occurred while fetching the cart"}

    # ============================== add item to cart ========================
    # edited to handle adding the custom cake to the cart
    def add_item_to_cart(self, customer_email, product_id=None, quantity=1, custom_cake_id=None):
        try:
            # Validate if either product_id or custom_cake_id is provided
            if not product_id and not custom_cake_id:
                return {"error": "(repo) product_id or custom_cake_id must be provided"}

            # Cart retrieval
            cart = Cart.query.filter_by(customeremail=customer_email).first()
            if not cart:
                return {"error": "(repo) Cart not found for this customer"}

            # Handling normal product addition
            if product_id:
                product = Inventory.query.get(product_id)
                if not product:
                    return {"error": "(repo) Product not found"}
                    
                cart_item = CartItems.query.filter_by(cartid=cart.cartid, productid=product_id).first()
                if cart_item:  # Product already in cart
                    cart_item.quantity += quantity
                else:  # New product
                    cart_item = CartItems(
                        cartid=cart.cartid,
                        productid=product_id,
                        quantity=quantity,
                        price=product.price,
                    )
                    db.session.add(cart_item)

            # Handling customized cake addition
            elif custom_cake_id:
                custom_cake = CustomizeCake.query.get(custom_cake_id)
                if not custom_cake:
                    return {"error": "(repo) Customized cake not found"}

                cart_item = CartItems(
                    cartid=cart.cartid,
                    customcakeid=custom_cake_id,
                    quantity=quantity,
                    price=custom_cake.price,  # Assuming CustomizeCake has a price attribute
                )
                db.session.add(cart_item)

            # Commit changes to the database
            db.session.commit()
            return {"message": f"Added to cart successfully, cart id: {cart.cartid}"}

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return {"error": f"(repo) Can't add item to cart: {str(e)}"}


    # =========================================================================================

    # ============================== remove item from cart ===================
    def remove_from_cart(self, customer_email, product_id):
        try:
            # ------- get cart --------
            cart = Cart.query.filter_by(customeremail=customer_email).first()
            if not cart:
                return {"error": "(repo) Cart not found for this customer"}
            # ------ item in cart --------
            cart_item = CartItems.query.filter_by(
                cartid=cart.cartid, productid=product_id
            ).first()
            if not cart_item:
                return {"error": "(repo) Item not found in the cart"}
            # ---------------------------
            db.session.delete(cart_item)
            db.session.commit()
            return {"message": "Item removed from cart successfully"}

        except Exception as e:
            db.session.rollback()
            return {
                "error": "error occurred while removing the item from the cart",
                "error_details": str(e),
            }

    # ===========================================================================================================

    # ====================== Raw materials ========================
    def get_raw_materials(self):
        raw_materials = Rawmaterials.query.all()

        # Serialize raw materials into dictionaries
        serialized_data = [material.as_dict() for material in raw_materials]

        return serialized_data

    # ===========================================================

    # --------------------------- Create custom cake -------------------------
    def create_custom_cake(self, customer_email, data):
        try:
            cake_shape = data.get("cakeshape")
            cake_size = data.get("cakesize")
            cake_type = data.get("caketype")
            cake_flavor = cake_type  # Assuming type is flavor
            message = data.get("message", "")
            layers = data.get("layers", [])
            num_layers = len(layers)

            # Validate cake shape, size, and type
            if not cake_shape or not cake_size or not cake_type:
                return {
                    "error": "Cake shape, size, and type are required fields.",
                    "message": "An error occurred while creating the custom cake."
                }

            # Validate that there are enough layers
            if num_layers < 1:  # Assuming at least two layers are required
                return {
                    "error": "At least 1 layers are required for the custom cake.",
                    "message": "Not enough segments"
                }
            print(1)
            # Calculate price for the custom cake
            total_price = 0.0
            for layer in layers:
                inner_fillings = layer.get("innerFillings", "")
                inner_toppings = layer.get("innerToppings", "")
                outer_coating = layer.get("outerCoating", "")
                outer_toppings = layer.get("outerToppings", "")

                if inner_fillings:
                    filling_price = (
                        db.session.query(Rawmaterials.price)
                        .filter_by(item=inner_fillings)
                        .scalar()
                        or 0.0
                    )
                    total_price += filling_price

                if inner_toppings:
                    topping_price = (
                        db.session.query(Rawmaterials.price)
                        .filter_by(item=inner_toppings)
                        .scalar()
                        or 0.0
                    )
                    total_price += topping_price

                if outer_coating:
                    coating_price = (
                        db.session.query(Rawmaterials.price)
                        .filter_by(item=outer_coating)
                        .scalar()
                        or 0.0
                    )
                    total_price += coating_price

                if outer_toppings:
                    topping_price = (
                        db.session.query(Rawmaterials.price)
                        .filter_by(item=outer_toppings)
                        .scalar()
                        or 0.0
                    )
                    total_price += topping_price

            # Essentials
            essentials = {
                "cakeshape": cake_shape,
                "cakesize": cake_size,
                "cakeflavor": cake_flavor,
            }

            for key, value in essentials.items():
                if value:  # Ensure the value is provided
                    essential_price = (
                        db.session.query(Rawmaterials.price)
                        .filter_by(item=value)
                        .scalar()
                        or 0.0
                    )
                    total_price += essential_price
            

            # Create the parent CustomizeCake record
            new_customized_cake = CustomizeCake(
                numlayers=num_layers,
                customeremail=customer_email,
                cakeshape=cake_shape,
                cakesize=cake_size,
                cakeflavor=cake_flavor,
                message=message,
                price=total_price,  # Save calculated price here
            )
            db.session.add(new_customized_cake)
            db.session.commit()  # Commit to generate ID

            self.add_item_to_cart(customer_email=customer_email, product_id=None, quantity=1, custom_cake_id=new_customized_cake.customizecakeid)
        
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
                    outertoppings=outer_toppings,
                )
                db.session.add(new_layer)

            db.session.commit()

            return {
                "message": "Cake customization created successfully!",
                "customizecakeid": new_customized_cake.customizecakeid,
                "totalprice": total_price,
            }

        except Exception as e:
            # Rollback all changes if any error occurs
            db.session.rollback()

            # Return an error response
            return {
                "message": "An error occurred while creating the custom cake.",
                "error": str(e),
            }


    # --------------------------- Create custom cake -------------------------

    
    # --------------------------- Check then Edit Customer Data ---------------------------

    #--------- Check customer present or not in database ---------
    def check_customer(self, customer_email):
    
        # Validate input
        if not customer_email:
            return {
                "message": "Customer email is required.",
                "status": "error"
            }, 400

        # Query the database for the user
        user = CustomerUser.query.filter_by(customeremail=customer_email).first()

        # Handle user not found
        if not user:
            return {
                "message": f"No user found with email: {customer_email}",
                "status": "error"
            }, 404

        # Check for data completeness
        missing_fields = []
        if not user.firstname:
            missing_fields.append("firstname")
        if not user.lastname:  
            missing_fields.append("lastname")
        if not user.phonenum:  
            missing_fields.append("phonenum")
        if not user.addressgooglemapurl:  
            missing_fields.append("addressgooglemapurl")

        if missing_fields:
            return {
                "message": "User's data is incomplete.",
                "status": "error",
                "missing_fields": missing_fields  # Provide details about missing fields
            }, 422  # 422: Unprocessable Entity

        # User exists and data is complete
        return {
            "message": f"User with firstname {user.firstname} is present in the database with completed data.",
            "status": "success"
        }, 200


        

    # --------- Check customer data for reviewing ---------
    def check_customer_data(self, customer_email):
        # Query the database for the customer user
        user = CustomerUser.query.filter_by(customeremail=customer_email).first()
    
        # Handle case where user is not found
        if not user:
            return {
                "message": "User not found",
                "status": "error"
            }, 400
    
        # Return user data if found
        return {
            "message": "User data retrieved successfully",
            "status": "success",
            "data": {
                "firstname": user.firstname,
                "lastname": user.lastname,  # Example: Include more fields if needed
                "phonenum":user.phonenum,
                "addressgooglemapurl":user.addressgooglemapurl
            }
        }, 200

    # --------- Change customer data ---------
    def change_customer_data(self, customer_email, data):
        # Extract the customer data from the input
        firstname = data.get("firstname", "")
        lastname = data.get("lastname", "")
        phonenum = data.get("phonenum", "")
        addressgooglemapurl = data.get("addressgooglemapurl", "")
        # If password is part of the update
        #password = data.get("password", "")

        try:
            # Retrieve the customer based on email
            user = CustomerUser.query.filter_by(
                customeremail=customer_email).first()

            if not user:
                return {"message": "User not found", "status": "error"}, 404

            # Update fields if provided
            if firstname:
                user.firstname = firstname
            if lastname:
                user.lastname = lastname
            if phonenum:
                user.phonenum = phonenum
            if addressgooglemapurl:
                user.addressgooglemapurl = addressgooglemapurl

            # If a new password is provided, hash it and update it
            #if password:
                # hashed_password = self.hash_password(password)  # Ensure you
                # have a hash function
            #    user.password = (
            #        password  # Assuming 'password' is the correct field name
            #    )

            # Commit the changes to the database
            db.session.commit()

            return {
                "message": "User's data updated successfully",
                "status": "success",
            }, 200

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return {
                "message": "An error occurred while editing user data",
                "error": str(e),
                "status": "error",
            }, 500

            # -------------------------------------------------------------------------------

    """ ============================ User Reset/Change password =============================== """

    def change_password(self, data):
        email = data.get("email")
        domain = email.split("@")[1]

        if domain == "cakerybaker.com":
            user = BakeryUser.query.filter_by(bakeryemail=email).first()
            role = "baker"
        elif domain == "gmail.com":
            user = CustomerUser.query.filter_by(customeremail=email).first()
            role = "customer"
        elif domain == "cakerydelivery.com":
            user = DeliveryUser.query.filter_by(deliveryemail=email).first()
            role = "delivery"
        else:
            return {"message": "Invalid email domain", "status": "error"}, 400

        try:
            if not user:
                return {
                    "message": "User not found please sign up",
                    "status": "error",
                }, 401

            new_pass = data.get("newpassword")
            new_pass_confirm = data.get(
                "newpasswordconfirm")  # Fixed typo here

            # Check if passwords match
            if new_pass != new_pass_confirm:
                return {"message": "Passwords do not match",
                        "status": "error"}, 400

            # Assuming you want to hash the password before saving it
            hashed_password = self.hash_password(
                new_pass
            )  # Replace with actual hashing logic

            # Update the user's password
            if role == "baker":
                user.bakerypassword = hashed_password
            elif role == "customer":
                user.customerpassword = hashed_password
            elif role == "delivery":
                user.deliverypassword = hashed_password

            # Commit the changes to the database
            db.session.commit()

            return {
                "message": "Password changed successfully",
                "status": "success",
            }, 200

        except Exception as e:
            return {
                "message": f"An error occurred: {str(e)}", "status": "error"}, 500
            # -------------------------------------------------------------------------------

    """ ============================ User reset password_send email=============================== """

    def check_user(self, data):
        # Email Configuration
        email = data.get("email")
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = os.getenv("SMTP_PORT")
        EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

        # Check if user exists
        user = CustomerUser.query.filter_by(customeremail=email).first()
        if not user:
            return {"message": "User not found", "status": "error"}, 404

        # Creating the reset token 
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))  # Use a secret key for token signing
        token = serializer.dumps(email, salt='password-reset')  # Use the user's email and a salt to generate the token

        # Create reset link (Link will be updated after deployment)
        reset_link = f"https://your-app.com/resetPassword/{token}"

        # Email content
        subject = "Password Reset Request"
        body = f"Hello {user.firstname},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request a password reset, please ignore this email."

        # Send email
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            return {
                "message": "Password reset email sent successfully",
                "status": "success",
            }, 200

        except Exception as e:
            print(f"Error sending email: {e}")
            return {
                "message": "Failed to send email",
                "error": str(e),
                "status": "error",
            }, 500


    def verify_reset_token(self,token):
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        try:
            email = serializer.loads(token, salt='password-reset', max_age=3600)  # 1-hour expiration
            return email
        except SignatureExpired:
            return None  # Token has expired
        except BadSignature:
            return None  # Invalid token


    """============================ get notifications ==============================="""

    def get_notifications(self, customer_email):
        try:
            notifications = Notification.query.filter_by(
                customer_email=customer_email
            ).all()
            # return only id and message
            result = [
                {"id": notification.id, "message": notification.message}
                for notification in notifications
            ]
            return result
        except Exception as e:
            return {"error": f"(repo) error getting notifications: {e}"}, 500

    def get_customer_name(self, customer_email):
        try:
            customer = CustomerUser.query.filter_by(
                customeremail=customer_email
            ).first()
            name = customer.firstname + " " + customer.lastname
            return name
        except Exception as e:
            print(f"(repo) can't get customer name: {e}")
            return None

    def increment_quantity(self, customer_email, product_id, action):
        try:
            #  cart for the customer
            cart = Cart.query.filter_by(customeremail=customer_email).first()
            if not cart:
                return {"message": "Cart not found"}, 404
            #  cart id and product id
            cart_item = CartItems.query.filter_by(
                cartid=cart.cartid, productid=product_id
            ).first()
            if cart_item:
                if action == "increment":
                    cart_item.quantity += 1
                elif action == "decrement" and cart_item.quantity == 1:
                    db.session.delete(cart_item)
                elif action == "decrement" and cart_item.quantity > 0:
                    cart_item.quantity -= 1
                db.session.commit()
                return {
                    "message": "Quantity updated successfully",
                    "new_quantity": cart_item.quantity,
                }, 200
            else:
                return {"message": "Cart item not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error updating quantity: {e}"}, 500

    """============================ add user review ==============================="""

    def place_review(self, customer_email, rating, product_id):
        try:
            # Validate customer_email exists
            customer = (
                db.session.query(CustomerUser)
                .filter_by(customeremail=customer_email)
                .first()
            )
            if not customer:
                return {"message": "Customer does not exist",
                        "status": "error"}, 404

            # Validate product_id exists
            product = (
                db.session.query(Inventory).filter_by(
                    productid=product_id).first()
            )
            if not product:
                return {"message": "Product does not exist",
                        "status": "error"}, 404

            # Validate rating is within acceptable range
            if not (1 <= rating <= 5):
                return {
                    "message": "Rating must be between 1 and 5",
                    "status": "error",
                }, 400

            existing_review = (
                db.session.query(Review)
                .filter_by(customeremail=customer_email, productid=product_id)
                .first()
            )
            if existing_review:
                existing_review.rating = rating
                db.session.commit()
                return {
                    "message": "User rating updated successfully",
                    "status": "success",
                }, 200
            # Create new review
            new_review = Review(
                customeremail=customer_email, rating=rating, productid=product_id
            )

            db.session.add(new_review)
            db.session.commit()

            return {
                "message": "User rating added successfully",
                "status": "success",
            }, 201

        except Exception as e:
            db.session.rollback()  # Ensure the transaction is rolled back in case of failure
            return {
                "message": "An error occurred",
                "error": str(e),
                "status": "error",
            }, 500
