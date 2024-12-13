from app.Repositories.delivery_repository import DeliveryRepository
from app.Repositories.order_repository import OrderRepository
from app.Services.order_service import OrderService


class DeliveryService:
    def __init__(self):
        self.delivery_repo = DeliveryRepository()
        # self.order_repo = OrderRepository()
        # self.order_service = OrderService()
    
    def view_assigned_orders(self,delivery_email):
        return self.delivery_repo.get_assigned_orders(delivery_email)