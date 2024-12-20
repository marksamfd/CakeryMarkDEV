from app.Repositories.customer_repository import CustomerRepository
from app.Repositories.order_repository import OrderRepository


class CustomerService:
    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.order_repo = OrderRepository()

    # ----------------- get all products ---------------------
    def list_products(self):
        return self.customer_repo.get_all_products()

    # ------------------- product detail -------------------
    def view_product_details(self, product_id):
        return self.customer_repo.get_product_by_id(product_id)

    # ------------------- get cart data -------------------
    def view_cart(self, customer_email):
        return self.customer_repo.get_cart(customer_email)

    # ------------------- add to cart -------------------
    def add_to_cart(
        self, customer_email, product_id, quantity, custom_cake_id=None
    ):  # included custom_cake_id but with none as default to avoid error
        return self.customer_repo.add_item_to_cart(
            customer_email, product_id, quantity, custom_cake_id
        )

    # ------------------- remove from cart -------------------
    def remove_from_cart(self, customer_email, product_id):
        return self.customer_repo.remove_from_cart(customer_email, product_id)

    # ------------------- make custom cake  -------------------
    def create_custom_cake(self, customer_email, data):
        return self.customer_repo.create_custom_cake(customer_email, data)

    # ------------------- view raw materials -------------------
    def view_raw_materials(self):
        return self.customer_repo.get_raw_materials()

    # ------------------- make order -------------------
    def checkout(self, customer_email, voucher_code):
        cart = self.customer_repo.get_cart(customer_email)
        if "error, cart not found" in cart:
            return cart  # Return error if cart not found
        cart_items = cart.get("items", [])
        return self.order_repo.create_order(
            customer_email, cart_items, voucher_code)

    # ------------------- view customer orders -------------------
    def view_customer_orders(self, customer_email):
        return self.order_repo.get_orders_by_customer(customer_email)
    # ------------------- Update/Edit customer data -------------------
    def get_user(self,customer_email):
        return self.customer_repo.check_customer(customer_email)

    def get_data(self,customer_email):
        return self.customer_repo.check_customer_data(customer_email)

    def update_data(self, customer_email,data):
        return self.customer_repo.change_customer_data(customer_email,data)
    
    # ----------- User forget password -----------
    def new_password(self, data):
        return self.customer_repo.change_password(data)
    def verify_token(self,token):
        return self.customer_repo.verify_reset_token(token)
    def send_email(self, data):
        return self.customer_repo.check_user(data)

    # ----------- my notification -----------
    def view_notifications(self, customer_email):
        return self.customer_repo.get_notifications(customer_email)

    def get_customer_name(self, customer_email):
        return self.customer_repo.get_customer_name(customer_email)

    def incrementQuantity(self, data, customer_email):
        customer_email = customer_email
        product_id = data["product_id"]
        action = data["action"]
        return self.customer_repo.increment_quantity(
            customer_email, product_id, action)

    def add_review(self, customer_email, rating, product_id):
        return self.customer_repo.place_review(
            customer_email, rating, product_id)
