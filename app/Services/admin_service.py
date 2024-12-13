from app.Repositories.order_repository import OrderRepository
# from app.Repositories.delivery_repository import DeliveryRepository
# from app.Repositories.user_repository import UserRepository
from app.Repositories.admin_repository import AdminRepository



class AdminService:
    def __init__(self):
        self.admin_repo = AdminRepository()
        self.order_repo = OrderRepository()
        # self.delivery_repo = DeliveryRepository()
        # self.user_repo = UserRepository()

    def get_users(self):
        return self.admin_repo.get_staff_users()
    
    def add_user(self,role,name,email,phone,password):
        if role == "baker":
            return self.admin_repo.add_bakery_user(name,email,phone,password)
        elif role == "delivery":
            return self.admin_repo.add_delivery_user(name,email,phone,password)
    

    def delete_user(self,role,email):
        if role == "baker":
            return self.admin_repo.delete_baker_user(email)
        elif role == "delivery":
            return self.admin_repo.delete_delivery_user(email)
       
    
