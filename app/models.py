from app.db import db

from datetime import datetime, timezone


""" The main difference here is that we are dealing with the database as models, where each table
is represented by a class, the class taking the db.model from the initialized db instance in the db.py file.
The class has the table name, and the columns as attributes, and the relationships as attributes as well.
The as_dict() method is used to convert the object to a dictionary (all attributes will be key and the value),
to be used in the services file to return the data as a dictionary as this JSON format will be sent to the frontend. Passwords are excluded from the dictionary response,
but accessed from the model.
"""


# Admin model
class Admin(db.Model):
    __tablename__ = "admin"

    adminemail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)


# BakeryUser model
class BakeryUser(db.Model):
    __tablename__ = "bakeryuser"

    bakeryemail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phonenum = db.Column(db.String(15))
    addresstext = db.Column(db.Text)
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())

    def as_dict(self):
        return {
            "bakeryemail": self.bakeryemail,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phonenum": self.phonenum,
            "addresstext": self.addresstext,
            "createdat": self.createdat.isoformat() if self.createdat else None,
        }


# CustomerUser model
class CustomerUser(db.Model):
    __tablename__ = "customeruser"

    customeremail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255),nullable=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phonenum = db.Column(db.String(15))
    addressgooglemapurl = db.Column(db.Text)
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())
    fcm_token = db.Column(db.String(255))

    # Relationships
    carts = db.relationship(
        "Cart",
        backref="customer",
        cascade="all, delete-orphan")
    orders = db.relationship(
        "Orders",
        backref="customer",
        cascade="all, delete-orphan")
    reviews = db.relationship(
        "Review", backref="customer", cascade="all, delete-orphan"
    )

    def as_dict(self):
        return {
            "customeremail": self.customeremail,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phonenum": self.phonenum,
            "addressgooglemapurl": self.addressgooglemapurl,
            "createdat": self.createdat.isoformat() if self.createdat else None,
        }


# CustomCake model
class CustomizeCake(db.Model):

    customizecakeid = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    numlayers = db.Column(db.Integer, nullable=False)
    customeremail = db.Column(
        db.String(255), db.ForeignKey("customeruser.customeremail")
    )
    cakeshape = db.Column(db.String(255), nullable=False)
    cakesize = db.Column(db.String(255), nullable=False)
    cakeflavor = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(500))
    price = db.Column(db.Integer())
    # Relationships
    layers = db.relationship(
        "Customize_Cake_Layers", backref="custom_cake", cascade="all, delete-orphan"
    )

    def as_dict(self):
        return {
            "customcakeid": self.customcakeid,
            "numlayers": self.numlayers,
            "cakeshape": self.cakeshape,
            "cakesize": self.cakesize,
            "cakeflavor": self.cakeflavor,
            "message": self.message,
        }


# Cart model
class Cart(db.Model):
    __tablename__ = "cart"

    cartid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customeremail = db.Column(
        db.String(255), db.ForeignKey("customeruser.customeremail")
    )

    # Relationships
    cart_items = db.relationship(
        "CartItems", backref="cart", cascade="all, delete-orphan"
    )

    def as_dict(self):
        return {"cartid": self.cartid, "customeremail": self.customeremail}


# CartItems model
class CartItems(db.Model):
    __tablename__ = "cartitems"

    cartitemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cartid = db.Column(db.Integer, db.ForeignKey("cart.cartid"))
    productid = db.Column(db.Integer, db.ForeignKey("inventory.productid"),nullable=True)
    customcakeid = db.Column(
        db.Integer, db.ForeignKey("customize_cake.customizecakeid"),nullable=True
    )
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def as_dict(self):
        return {
            "cartitemid": self.cartitemid,
            "cartid": self.cartid,
            "productid": self.productid,
            "customcakeid": self.customcakeid,
            "quantity": self.quantity,
            "price": self.price,
        }


# CakeLayer model
class Customize_Cake_Layers(db.Model):
    __tablename__ = "customize_cake_layer"

    customizecakeid = db.Column(
        db.Integer, db.ForeignKey("customize_cake.customizecakeid"), primary_key=True
    )
    layer = db.Column(db.Integer, primary_key=True)
    innerfillings = db.Column(db.String(255), nullable=False)
    innertoppings = db.Column(db.String(255), nullable=False)
    outercoating = db.Column(db.String(255), nullable=False)
    outertoppings = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {
            "customizecakeid": self.customizecakeid,
            "layer": self.layer,
            "innerfillings": self.innerfillings,
            "innertoppings": self.innertoppings,
            "outercoating": self.outercoating,
            "outertoppings": self.outertoppings,
        }


# Inventory model
class Inventory(db.Model):
    __tablename__ = "inventory"

    productid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    category = db.Column(db.String(255))
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())
    imgpath = db.Column(db.String(255))

    reviews = db.relationship(
        "Review", backref="inventory", cascade="all, delete-orphan"
    )

    def as_dict(self):
        return {
            "productid": self.productid,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "createdat": self.createdat.isoformat() if self.createdat else None,
            "image": self.imgpath,
        }


# Raw Materials Model
class Rawmaterials(db.Model):
    __tablename__ = "rawmaterials"

    item = db.Column(db.String, primary_key=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)

    def as_dict(self):
        return {
            "item": self.item,
            "price": self.price,
            "category": self.category,
        }


# Orders model
class Orders(db.Model):
    __tablename__ = "orders"

    orderid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customeremail = db.Column(
        db.String(255), db.ForeignKey("customeruser.customeremail")
    )
    deliveryemail = db.Column(
        db.String(255), db.ForeignKey("deliveryuser.deliveryemail")
    )
    totalprice = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50))
    orderdate = db.Column(db.DateTime, default=db.func.current_timestamp())
    deliverydate = db.Column(db.DateTime)

    # Relationships
    payments = db.relationship(
        "Payment",
        backref="order",
        cascade="all, delete-orphan")
    order_items = db.relationship(
        "OrderItems", backref="order", cascade="all, delete-orphan"
    )

    def as_dict(self):
        return {
            "orderid": self.orderid,
            "customeremail": self.customeremail,
            "deliveryemail": self.deliveryemail,
            "totalprice": self.totalprice,
            "status": self.status,
            "orderdate": self.orderdate.isoformat() if self.orderdate else None,
            "deliverydate": (
                self.deliverydate.isoformat() if self.deliverydate else None
            ),
        }


# DeliveryUser model
class DeliveryUser(db.Model):
    __tablename__ = "deliveryuser"

    deliveryemail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phonenum = db.Column(db.String(15))
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())

    def as_dict(self):
        return {
            "deliveryemail": self.deliveryemail,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phonenum": self.phonenum,
            "createdat": self.createdat.isoformat() if self.createdat else None,
        }


# DeliveryAssignments model
class DeliveryAssignments(db.Model):
    __tablename__ = "delivery_assignments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deliveryemail = db.Column(
        db.String(255), db.ForeignKey("deliveryuser.deliveryemail"), nullable=False
    )
    orderid = db.Column(
        db.Integer,
        db.ForeignKey("orders.orderid"),
        nullable=False)

    # Relationships
    delivery_user = db.relationship("DeliveryUser", backref="assignments")
    order = db.relationship("Orders", backref="assigned_delivery")

    def as_dict(self):
        return {
            "id": self.id,
            "deliveryemail": self.deliveryemail,
            "orderid": self.orderid,
        }


# OrderItems model
class OrderItems(db.Model):
    __tablename__ = "orderitems"
    orderitemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey("orders.orderid"))
    productid = db.Column(db.Integer, db.ForeignKey("inventory.productid"))
    customcakeid = db.Column(
        db.Integer, db.ForeignKey("customize_cake.customizecakeid")
    )  # Correct column
    quantity = db.Column(db.Integer, nullable=False)
    priceatorder = db.Column(db.Numeric(10, 2))

    def as_dict(self):
        return {
            "orderitemid": self.orderitemid,
            "orderid": self.orderid,
            "productid": self.productid,
            "customizecakeid": self.customizecakeid,
            "quantity": self.quantity,
            "priceatorder": self.priceatorder,
        }


# Payment model
class Payment(db.Model):
    __tablename__ = "payment"

    paymentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey("orders.orderid"))
    deposit = db.Column(db.Numeric(10, 2), nullable=False)
    restofprice = db.Column(db.Numeric(10, 2), nullable=False)
    paymentdate = db.Column(db.DateTime, default=db.func.current_timestamp())

    def as_dict(self):
        return {
            "paymentid": self.paymentid,
            "orderid": self.orderid,
            "deposit": self.deposit,
            "restofprice": self.restofprice,
            "paymentdate": self.paymentdate.isoformat() if self.paymentdate else None,
        }


# Review model
class Review(db.Model):
    __tablename__ = "review"

    reviewid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productid = db.Column(db.Integer, db.ForeignKey("inventory.productid"))
    customeremail = db.Column(
        db.String(255), db.ForeignKey("customeruser.customeremail")
    )
    rating = db.Column(db.Integer, nullable=False)
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())

    def as_dict(self):
        return {
            "reviewid": self.reviewid,
            "productid": self.productid,
            "customeremail": self.customeremail,
            "rating": self.rating,
            "createdat": self.createdat.isoformat() if self.createdat else None,
        }


# Voucher model
class Voucher(db.Model):
    __tablename__ = "voucher"

    vouchercode = db.Column(db.String(255), primary_key=True)
    discountpercentage = db.Column(db.Numeric(5, 2), nullable=False)

    def as_dict(self):
        return {
            "vouchercode": self.vouchercode,
            "discountpercentage": self.discountpercentage,
        }


# ---------- notification ---------------


class OTP(db.Model):
    __tablename__ = "otp"

    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(100), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.orderid"))

    def as_dict(self):
        return {
            "id": self.id,
            "customer_email": self.customer_email,
            "otp_code": self.otp_code,
            "expiry_time": self.expiry_time.isoformat(),
            "is_used": self.is_used,
            "created_at": self.created_at.isoformat(),
        }


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def as_dict(self):
        return {
            "id": self.id,
            "customer_email": self.customer_email,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }
