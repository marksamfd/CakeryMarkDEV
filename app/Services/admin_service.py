from app.Repositories.order_repository import OrderRepository
from app.Repositories.admin_repository import AdminRepository
from app.Repositories.delivery_repository import DeliveryRepository


class AdminService:
    def __init__(self):
        delivery_repo = DeliveryRepository()
        self.admin_repo = AdminRepository(delivery_repo=delivery_repo)
        self.order_repo = OrderRepository()

    # -------- get list of staff users  ------
    def get_users(self):
        return self.admin_repo.get_staff_users()

    def add_user(self, data):
        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        role = data["role"]

        if role == "baker":
            return self.admin_repo.add_bakery_user(
                firstname, lastname, email, phone, password
            )
        elif role == "delivery":
            return self.admin_repo.add_delivery_user(
                firstname, lastname, email, phone, password
            )
        else:
            return {
                f"passed role is wrong, error in adding user (service)"}, 400

    def delete_user(self, data):
        role = data["role"]
        email = data["email"]
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
    def edit_product(self, data):
        product_id = data["product_id"]
        rawItem = data["rawItem"]
        price = data["price"]
        if rawItem:
            return self.admin_repo.edit_product(
                product_id=None, rawItem=rawItem, price=price
            )
        else:
            return self.admin_repo.edit_product(
                product_id, rawItem=None, price=price)

    def add_voucher(self, data):
        discount = data["discount"]
        voucher_code = data["voucher_code"]
        return self.admin_repo.add_voucher(voucher_code,discount)

    def edit_vocher(self, data):
        voucher_id = data["voucher_id"]
        discount = data["discount"]
        return self.admin_repo.edit_voucher(voucher_id, discount)

    def delete_voucher(self, data):
        voucher_id = data["voucher_id"]
        return self.admin_repo.delete_voucher(voucher_id)

    def get_vouchers(self):
        return self.admin_repo.get_vouchers()

    def dashboard_data(self):
        return self.admin_repo.get_dashboard_data()
