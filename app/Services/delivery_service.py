from app.Repositories.delivery_repository import DeliveryRepository
from app.Repositories.order_repository import OrderRepository
from app.Services.otp_service import OTPService


class DeliveryService:
    def __init__(self, notifier):
        self.delivery_repo = DeliveryRepository()
        self.order_repo = OrderRepository()
        self.otp_service = OTPService(notifier)
        self.notifier = notifier

    def mark_order_status(self, order_id, new_status):
        result = self.order_repo.update_order_status(order_id, new_status)
        if "error" in result:
            return result

        # ---- Send notifications based on status ---- 
        customer_email = self.order_repo.get_customerEmail_by_order_id(order_id)
        if new_status == "delivered":
            otp_code = self.otp_service.generate_and_save_otp(customer_email, order_id)
            if not otp_code:
                return {"error": "Error generating OTP"}
            return "Order status updated successfully"

        elif new_status == "out_for_delivery":
            message = "Your order is out for delivery"
            self.notifier.notify_observers(customer_email, message)
            return "Order status updated successfully"

        return {"error": f"Cannot update to status: {new_status}"}


    def view_assigned_orders(self, delivery_email):
        return self.delivery_repo.get_assigned_orders(delivery_email)

    def get_deliveryman_name(self, delivery_email):
        return self.delivery_repo.get_deliveryman_name(delivery_email)


