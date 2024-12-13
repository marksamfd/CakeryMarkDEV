from app.models import DeliveryUser, BakeryUser, Inventory, Voucher, Rawmaterials
from app.db import db
from argon2 import PasswordHasher

encrypt = PasswordHasher()



class AdminRepository:
    ''' ============================ get all staff users =============================== '''
    # ---- get all staff users ----
    def  get_staff_users(self):
        stafflist = {}
        delivery_users = DeliveryUser.query.all()
        for user in delivery_users:
            stafflist[user.email] = {
                "name": user.name,
                "email" : user.email,
                "phone" : user.phone,
                "role": "delivery",
            }
        bakery_users = BakeryUser.query.all()  
        for user in bakery_users:
            stafflist[user.email] = {
                "name": user.name,
                "email" : user.email,
                "phone" : user.phone,
                "role": "baker",
            }
        return stafflist
    
    ''' ============================ add staff user =============================== '''
    # ---- add baker user ----
    def add_bakery_user(self, name, email, phone, password):
        hashed_password = encrypt.hash(password)
        bakery_user = BakeryUser(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(bakery_user)
        db.session.commit()
        return bakery_user
    # ---- add delivery user ----
    def add_delivery_user(self, name, email, phone, password):
        hashed_password = encrypt.hash(password)
        delivery_user = DeliveryUser(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(delivery_user)
        db.session.commit()
        return delivery_user
    
    ''' ============================ delete staff user =============================== '''
    # ---- delete baker user ----
    def delete_baker_user(self, email):
        baker = BakeryUser.query.filter_by(email=email).first()
        db.session.delete(baker)
        db.session.commit()
        return {"message": "baker deleted successfully"}
    # ---- delete delivery user ----
    def delete_delivery_user(self, email):
        delivery = DeliveryUser.query.filter_by(email=email).first()
        db.session.delete(delivery)
        db.session.commit()
        return {"message": "delivery deleted successfully"}

        
    ''' ============================ add/edit voucher =============================== '''
    # ---- add voucher ----
    def add_voucher(self, voucher_code, discount_percentage):
        voucher = Voucher(voucher_code=voucher_code, discount_percentage=discount_percentage)
        db.session.add(voucher)
        db.session.commit()
        return voucher
    # ---- edit voucher ----
    def edit_voucher(self, voucher_code, discount_percentage):
        voucher = Voucher.query.filter_by(voucher_code=voucher_code)
        if voucher:
            voucher.discount_percentage = discount_percentage
            db.session.commit()
            return voucher
        return None

    def delete_voucher(self, voucher_code):
        voucher = Voucher.query.filter_by(voucher_code=voucher_code)
        if voucher:
            db.session.delete(voucher)

    ''' ============================ edit raw product or raw materials prices =============================== '''
    # ------ get all raw products ------
    def raw_materials(self):
        rawItems = Rawmaterials.query.all()
        raw_materials_list = {}
        for raw_product in rawItems:
            raw_materials_list[raw_product.raw_product_name] = {
                "price": raw_product.price,
                "quantity": raw_product.quantity,
            }
        return raw_materials_list
    