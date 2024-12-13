from app.models import DeliveryUser, BakeryUser, Admin
from app.db import db
from argon2 import PasswordHasher

encrypt = PasswordHasher()



class AdminRepository:
    ''' ============================ get all staff users =============================== '''
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
    def add_bakery_user(self, name, email, phone, password):
        hashed_password = encrypt.hash(password)
        bakery_user = BakeryUser(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(bakery_user)
        db.session.commit()
        return bakery_user
    def add_delivery_user(self, name, email, phone, password):
        hashed_password = encrypt.hash(password)
        delivery_user = DeliveryUser(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(delivery_user)
        db.session.commit()
        return delivery_user
    
    ''' ============================ delete staff user =============================== '''
    def delete_baker_user(self, email):
        baker = BakeryUser.query.filter_by(email=email).first()
        db.session.delete(baker)
        db.session.commit()
        return {"message": "baker deleted successfully"}
    def delete_delivery_user(self, email):
        delivery = DeliveryUser.query.filter_by(email=email).first()
        db.session.delete(delivery)
        db.session.commit()
        return {"message": "delivery deleted successfully"}

        
    
  
    