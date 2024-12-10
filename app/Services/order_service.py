from app.Repositories.order_repository import OrderRepository
from app.Repositories.delivery_repository import DeliveryRepository

class OrderService:
    def __init__(self):
        self.order_repo = OrderRepository()
        self.delivery_repo = DeliveryRepository()

    def create_order_from_cart(self, customer_email, cart_items, voucher_code=None):
        return self.order_repo.create_order(customer_email, cart_items, voucher_code)

    def update_order_status(self, order_id, status):
        return self.order_repo.update_order_status(order_id, status)

    def assign_delivery(self, order_id, delivery_email):
        return self.delivery_repo.assign_delivery_user(order_id, delivery_email)
