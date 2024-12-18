from app.Repositories.baker_repository import BakerRepository
from app.Services.order_service import OrderService


class BakerService:
    def __init__(self):
        self.baker_repo = BakerRepository()
        self.order_service = OrderService()

    # ----------- view all orders -----------
    def view_baker_orders(self):
        return self.baker_repo.get_all_orders()

    # ----------- view specific order -----------
    def view_specific_order(self, order_id):
        return self.baker_repo.get_order_details(order_id)

    # ----------- update order status & assign delivery user ------------
    def mark_order_prepared(self, order_id):
        result = self.baker_repo.update_order_status(
            order_id, "Prepared"
        )  # any input from the baker routes will be "Prepared"
        if "error" in result:
            return result

        # Assign a delivery user - currently None, can be handled as needed
        delivery_assignment = self.order_service.assign_delivery(order_id)
        return delivery_assignment
