from app.db import db

''' The main differnce here is that we are dealing with the database as models, where each table
is represented by a class, the class taking the db.model from the initialized db instance in the db.py file.
The class has the table name, and the columns as attributes, and the relationships as attributes as well.
The as_dict() method is used to convert the object to a dictionary (all attributes will be key and the vale ),
 to be used in the services file to return the data as a dictionary as this json format will be sent to frontend. passwords are excluded from the dictionary response, 
 but accsesed from the model
.'''

# Admin model
class Admin(db.Model):
    __tablename__ = 'admin'

    adminemail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)

# BakeryUser model
class BakeryUser(db.Model):
    __tablename__ = 'bakeryuser'

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
            "createdat": self.createdat.isoformat() if self.createdat else None}


# CustomerUser model
class CustomerUser(db.Model):
    __tablename__ = 'customeruser'

    customeremail = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phonenum = db.Column(db.String(15))
    addressgooglemapurl = db.Column(db.Text)
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    carts = db.relationship('Cart', backref='customer', cascade='all, delete-orphan')
    orders = db.relationship('Orders', backref='customer', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='customer', cascade='all, delete-orphan')
    def as_dict(self):
        return {
            "customeremail": self.customeremail,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phonenum": self.phonenum,
            "addressgooglemapurl": self.addressgooglemapurl,
            "createdat": self.createdat.isoformat() if self.createdat else None
        }


# Cart model
class Cart(db.Model):
    __tablename__ = 'cart'

    cartid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customeremail = db.Column(db.String(255), db.ForeignKey('customeruser.customeremail'))

    # Relationships
    cart_items = db.relationship('CartItems', backref='cart', cascade='all, delete-orphan')
    def as_dict(self):
        return {
            "cartid": self.cartid,
            "customeremail": self.customeremail
        }


# CartItems model
class CartItems(db.Model):
    __tablename__ = 'cartitems'

    cartitemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cartid = db.Column(db.Integer, db.ForeignKey('cart.cartid'))
    productid = db.Column(db.Integer, db.ForeignKey('inventory.productid'))
    customcakeid = db.Column(db.Integer, db.ForeignKey('customcake.customcakeid'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def as_dict(self):
        return {
            "cartitemid": self.cartitemid,
            "cartid": self.cartid,
            "productid": self.productid,
            "customcakeid": self.customcakeid,
            "quantity": self.quantity,
            "price": self.price
        }


# CustomCake model
class CustomCake(db.Model):
    __tablename__ = 'customcake'

    customcakeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numlayers = db.Column(db.Integer, nullable=False)
    sugarpaste = db.Column(db.String(255))
    coating = db.Column(db.String(255))
    topping = db.Column(db.String(255))

    # Relationships
    layers = db.relationship('CakeLayer', backref='custom_cake', cascade='all, delete-orphan')

    def as_dict(self):
        return {
            "customcakeid": self.customcakeid,
            "numlayers": self.numlayers,
            "sugarpaste": self.sugarpaste,
            "coating": self.coating,
            "topping": self.topping
        }


# CakeLayer model
class CakeLayer(db.Model):
    __tablename__ = 'cakelayer'

    layerid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customcakeid = db.Column(db.Integer, db.ForeignKey('customcake.customcakeid'))
    level = db.Column(db.Integer, nullable=False)
    flavor = db.Column(db.String(255))
    innerfilling = db.Column(db.String(255))
    nuts = db.Column(db.String(255))
    def as_dict(self):
        return {
            "layerid": self.layerid,
            "customcakeid": self.customcakeid,
            "level": self.level,
            "flavor": self.flavor,
            "innerfilling": self.innerfilling,
            "nuts": self.nuts
        }


# Inventory model
class Inventory(db.Model):
    __tablename__ = 'inventory'

    productid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    category = db.Column(db.String(255))
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())


    def as_dict(self):
        return {
            "productid": self.productid,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "createdat": self.createdat.isoformat() if self.createdat else None
        }


# Orders model
class Orders(db.Model):
    __tablename__ = 'orders'

    orderid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customeremail = db.Column(db.String(255), db.ForeignKey('customeruser.customeremail'))
    deliveryemail = db.Column(db.String(255), db.ForeignKey('deliveryuser.deliveryemail'))
    totalprice = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50))
    orderdate = db.Column(db.DateTime, default=db.func.current_timestamp())
    deliverydate = db.Column(db.DateTime)

    # Relationships
    payments = db.relationship('Payment', backref='order', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='order', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItems', backref='order', cascade='all, delete-orphan')

    def as_dict(self):
        return {
            "orderid": self.orderid,
            "customeremail": self.customeremail,
            "deliveryemail": self.deliveryemail,
            "totalprice": self.totalprice,
            "status": self.status,
            "orderdate": self.orderdate.isoformat() if self.orderdate else None,
            "deliverydate": self.deliverydate.isoformat() if self.deliverydate else None
        }


# DeliveryUser model
class DeliveryUser(db.Model):
    __tablename__ = 'deliveryuser'

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
            "createdat": self.createdat.isoformat() if self.createdat else None
        }


# Delivery assigments, which is spliitted table to have all orders the deliveryguy handles

class DeliveryAssignments(db.Model):
    __tablename__ = 'delivery_assignments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deliveryemail = db.Column(db.String(255), db.ForeignKey('deliveryuser.deliveryemail'), nullable=False)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.orderid'), nullable=False)

    # Relationships
    delivery_user = db.relationship('DeliveryUser', backref='assignments')
    order = db.relationship('Orders', backref='assigned_delivery')

    def as_dict(self):
        return {
            "id": self.id,
            "deliveryemail": self.deliveryemail,
            "orderid": self.orderid
        }





# OrderItems model
class OrderItems(db.Model):
    __tablename__ = 'orderitems'

    orderitemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.orderid'))
    productid = db.Column(db.Integer, db.ForeignKey('inventory.productid'))
    customcakeid = db.Column(db.Integer, db.ForeignKey('customcake.customcakeid'))
    quantity = db.Column(db.Integer, nullable=False)
    priceatorder = db.Column(db.Numeric(10, 2))
    
    def as_dict(self):
        return {
            "orderitemid": self.orderitemid,
            "orderid": self.orderid,
            "productid": self.productid,
            "customcakeid": self.customcakeid,
            "quantity": self.quantity,
            "priceatorder": self.priceatorder
        }

# Payment model
class Payment(db.Model):
    __tablename__ = 'payment'

    paymentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.orderid'))
    deposit = db.Column(db.Numeric(10, 2), nullable=False)
    restofprice = db.Column(db.Numeric(10, 2), nullable=False)
    paymentdate = db.Column(db.DateTime, default=db.func.current_timestamp())


    def as_dict(self):
        return {
            "paymentid": self.paymentid,
            "orderid": self.orderid,
            "deposit": self.deposit,
            "restofprice": self.restofprice,
            "paymentdate": self.paymentdate.isoformat() if self.paymentdate else None
        }

# Review model
class Review(db.Model):
    __tablename__ = 'review'

    reviewid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderid = db.Column(db.Integer, db.ForeignKey('orders.orderid'))
    customeremail = db.Column(db.String(255), db.ForeignKey('customeruser.customeremail'))
    rating = db.Column(db.Integer, nullable=False)
    createdat = db.Column(db.DateTime, default=db.func.current_timestamp())


    def as_dict(self):
        return {
            "reviewid": self.reviewid,
            "orderid": self.orderid,
            "customeremail": self.customeremail,
            "rating": self.rating,
            "createdat": self.createdat.isoformat() if self.createdat else None
        }

# Voucher model
class Voucher(db.Model):
    __tablename__ = 'voucher'

    vouchercode = db.Column(db.String(255), primary_key=True)
    discountpercentage = db.Column(db.Numeric(5, 2), nullable=False)

    def as_dict(self):
        return {
            "vouchercode": self.vouchercode,
            "discountpercentage": self.discountpercentage
        }
