from app.models import Inventory, Cart, CartItems,Rawmaterials,CustomizeCake,Customize_Cake_Layers,CustomerUser,Notification
from app.db import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class CustomerRepository:
    # ============================== get all products ==============================
    def get_all_products(self):
        try:
            products = Inventory.query.all()
            return [product.as_dict() for product in products]
        except Exception as e:
            print(f"(repo) can't get all products: {e}")
            return []
        
    #==============================================================================


    # ============================== get product by id ==============================
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
            cart = Cart.query.filter_by(customeremail=customer_email).first() # get the cart of the customer 
            if not cart:
                return {"error": "Cart not found"}
            
            cart_items = [
                {
                    "productid": item.productid,
                    "customcakeid": item.customcakeid,
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
        
    # ============================== add item to cart ==============================
    # edited to handle adding the custom cake to the cart 
    def add_item_to_cart(self, customer_email, product_id=None, quantity=1, custom_cake_id=None):
        try:
            # cart
            cart = Cart.query.filter_by(customeremail=customer_email).first()
            if not cart:
                return {"error": "(repo) Cart not found for this customer"}

            #  ---------- normal product  ------------
            if product_id:
                product = Inventory.query.get(product_id)
                if not product:
                    return {"error": "(repo) Product not found"}
                
                
                cart_item = CartItems.query.filter_by(cartid=cart.cartid, productid=product_id).first()
                if cart_item: # if the product is already in the cart
                    cart_item.quantity += quantity
                else: # if first time adding the product
                    cart_item = CartItems(
                        cartid=cart.cartid, 
                        productid=product_id, 
                        quantity=quantity, 
                        price=product.price
                    )
                    db.session.add(cart_item)

            # ---------- customized cake  ------------
            elif custom_cake_id:
                custom_cake = CustomizeCake.query.get(custom_cake_id)
                if not custom_cake:
                    return {"error": "(repo) Customized cake not found"}
                
                cart_item = CartItems(
                  cartid=cart.cartid, 
                  customcakeid=custom_cake_id, 
                  quantity=quantity, 
                  price=custom_cake.price  # Assuming CustomizeCake has a price attribute
                )
                db.session.add(cart_item)

            else: 
                return {"error": "(repo) product_id or custom_cake_id must be provided"}

            db.session.commit()
            return {"message": f"Added to cart successfully, cart id: {cart.cartid}"}
        except Exception as e:
            db.session.rollback()
            return {"error": f"(repo) Can't add item to cart: {e}"}

    # =========================================================================================


    # ============================== remove item from cart ==============================
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
    # ===========================================================================================================

    # ====================== Raw materials ========================
    def get_raw_materials(self):
        raw_materials = Rawmaterials.query.all()

        # Serialize raw materials into dictionaries
        serialized_data = [material.as_dict() for material in raw_materials]

        return serialized_data
    # ===========================================================


    # --------------------------- Create custom cake ---------------------------
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

        db.session.commit()

        return {"message": "Cake customization created successfully!", "customizecakeid": new_customized_cake.customizecakeid}

    # --------------------------- Create custom cake ---------------------------

    def change_customer_data(self,customer_email,data):
        
        email = data.get("email")
        password = data.get("password")

        # Validate required fields
        if not email or not password:
            return {
            "message": "Email and password are required",
            "status": "error"
            }, 400

        # Extract user domain
        domain = email.split("@")[1] if "@" in email else None

        if not domain:
            return {
            "message": "Invalid email format",
            "status": "error"
            }, 400

        role = None
        user = None

        # Define the queries for different user roles
        if domain == "cakery_admin.com":
            user = Admin.query.filter_by(adminemail=email).first()
            role = "admin"
        elif domain == "cakery_baker.com":
            user = BakeryUser.query.filter_by(bakeryemail=email).first()
            role = "baker"
            name = user.firstname
        elif domain == "gmail.com":
            user = CustomerUser.query.filter_by(customeremail=email).first()
            role = "customer"
            name = user.firstname
        elif domain == "cakery_delivery.com":
            user = DeliveryUser.query.filter_by(deliveryemail=email).first()
            role = "delivery"
            name = user.firstname
        else:
            return {
                "message": "Invalid email domain",
                "status": "error"
            }, 400

        try:
            # User not found
            if not user:
                return {
                    "message": "User not found",
                    "status": "error"
                }, 401

            # Compare the stored password and the input password
            stored_password = user.password
            #stored_password == password
            """ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ To be Edited later ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            """ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Caution ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """
            ''' I commented the condition above because the password is hashed and can't be compared directly '''
            #if self.verify_password(stored_password, password):
            # Create JWT token with role as an additional claim
            additional_claims = {"role": role}
            access_token = create_access_token(identity=email, additional_claims=additional_claims)
            return {
                    "message": "Sign-in successful",
                    "status": "success",
                    "firstname":name,
                    "role": role,
                    "access_token": access_token
                }, 200
            # else:
            #     return {
            #         "message": "Wrong Password",
            #         "status": "error"
            #     }, 401



        except Exception as e:
            return {
                "message": "An error occurred during sign-in",
                "error": str(e),
                "status": "error"
            }, 500

    # -------------------------------------------------------------------------------  


    def change_customer_data(self, customer_email, data):
    # Extract the customer data from the input
        firstname = data.get("firstname", "")
        lastname = data.get("lastname", "")
        phonenum = data.get("phonenum", "")
        addressgooglemapurl = data.get("addressgooglemapurl", "")
        password = data.get("password", "")  # If password is part of the update

        try:
            # Retrieve the customer based on email
            user = CustomerUser.query.filter_by(customeremail=customer_email).first()

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
            if password:
                #hashed_password = self.hash_password(password)  # Ensure you have a hash function
                user.password = password  # Assuming 'password' is the correct field name

            # Commit the changes to the database
            db.session.commit()

            return {"message": "User's data updated successfully", "status": "success"}, 200

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return {"message": "An error occurred while editing user data", "error": str(e), "status": "error"}, 500


               # -------------------------------------------------------------------------------  

    ''' ============================ User Reset/Change password =============================== '''

    def change_password(self,data):
        email = data.get("email")
        domain = email.split("@")[1]

        
        if domain == "cakery_baker.com":
            user = BakeryUser.query.filter_by(bakeryemail=email).first()
            role = "baker"
        elif domain == "gmail.com":
            user = CustomerUser.query.filter_by(customeremail=email).first()
            role = "customer"
        elif domain == "cakery_delivery.com":
            user = DeliveryUser.query.filter_by(deliveryemail=email).first()
            role = "delivery"
        else:
            return {
                "message": "Invalid email domain",
                "status": "error"
            }, 400

        try:
            if not user:
                return {
                    "message": "User not found please sign up",
                    "status": "error"
                }, 401

            new_pass = data.get("newpassword")
            new_pass_confirm = data.get("newpasswordconfirm")  # Fixed typo here

            # Check if passwords match
            if new_pass != new_pass_confirm:
                return {
                    "message": "Passwords do not match",
                    "status": "error"
                }, 400

            # Assuming you want to hash the password before saving it
            hashed_password = self.hash_password(new_pass)  # Replace with actual hashing logic

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
                "status": "success"
            }, 200

        except Exception as e:
            return {
                "message": f"An error occurred: {str(e)}",
                "status": "error"
            }, 500
               # -------------------------------------------------------------------------------  

    ''' ============================ User reset password_send email=============================== '''
    def check_user(self, data):
        # Email Configuration
        email = data.get("email")
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_ADDRESS = "ahmedabdelghany951@gmail.com"
        EMAIL_PASSWORD = '123umnft'
        
        # Check if user exists
        user = CustomerUser.query.filter_by(customeremail=email).first()
        if not user:
            return {"message": "User not found", "status": "error"}, 404

        # Create reset token (pseudo-code, replace with actual implementation)
        reset_token = self.generate_reset_token(email)  # Implement this function
        reset_link = f"https://your-app.com/reset-password?token={reset_token}"
        
        # Email content
        subject = "Password Reset Request"
        body = f"Hello {user.firstname},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request a password reset, please ignore this email."

        # Send email
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            return {"message": "Password reset email sent successfully", "status": "success"}, 200

        except Exception as e:
            return {"message": "Failed to send email", "error": str(e), "status": "error"}, 500
        



    '''============================ get notifications ==============================='''
    def get_notifications(self, customer_email):
        try:
            notifications = Notification.query.filter_by(customer_email=customer_email).all()
            # return only id and message
            result = [{"id": notification.id, "message": notification.message} for notification in notifications]
            return result
        except Exception as e:
            return {"error": f"(repo) error getting notifications: {e}"}, 500
        
    def get_customer_name(self, customer_email):
        try:
            customer = CustomerUser.query.filter_by(customeremail=customer_email).first()
            name = customer.firstname + " " + customer.lastname
            return name
        except Exception as e:
            print(f"(repo) can't get customer name: {e}")
            return None