from app.Repositories.order_repository import OrderRepository
from app.Repositories.admin_repository import AdminRepository




class AdminService:
    def __init__(self):
        self.admin_repo = AdminRepository()
        self.order_repo = OrderRepository()

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
    # ------ get list of customers from order repo ------
    def get_customers(self):
        return self.admin_repo.get_customers()

    # ------ get list of products & raw material------
    def get_products(self):
        return self.admin_repo.prducts_rawMats()
    # update product price
    def edit_product(self,price,product_id,rawItem=None):
        return self.admin_repo.edit_product(product_id,rawItem,price)
    

    def add_voucher(self,discount):
        return self.admin_repo.add_voucher(discount)
    def edit_vocher(self,voucher_id,discount):
        return self.admin_repo.edit_voucher(voucher_id,discount)
    def delete_voucher(self,voucher_id):
        return self.admin_repo.delete_voucher(voucher_id)
    def get_vouchers(self):
        return self.admin_repo.get_vouchers()
    
    