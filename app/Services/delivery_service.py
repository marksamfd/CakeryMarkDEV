from app.Repositories.delivery_repository import DeliveryRepository
from app.Repositories.order_repository import OrderRepository
from app.Services.order_service import OrderService
from app.Services.otp_service import OTPService
from app.utils.order_status_notifier import OrderStatusNotifier, PushNotificationObserver, DatabaseNotificationObserver


class DeliveryService:
    def __init__(self):
        self.delivery_repo = DeliveryRepository()
        self.order_repo = OrderRepository()
        self.order_service = OrderService()
        self.notifier = OrderStatusNotifier()
        self.otp_service = OTPService()
        self.notifier = OrderStatusNotifier()

        self.notifier.register_observer(PushNotificationObserver())
        self.notifier.register_observer(DatabaseNotificationObserver())
    

    def mark_order_status(self, order_id, new_status):
        result = self.order_repo.update_order_status(order_id, new_status)
        if "error" in result:
            return result

        # ----------- send notification to customer ------------
        if new_status == "delivered":
            customer_email = self.order_repo.get_customerEmail_by_order_id(order_id)
            otp_code = self.otp_service.generate_and_save_otp(customer_email)

            message = f"Your order has been delivered. Use OTP: {otp_code} to confirm"
            self.notifier.notify_observers(customer_email, message)
            return "Order status updated successfully"

        else:
            error = f"Order status cant' be updated to this status , status: {new_status}"
            return {"error": error}
        
        


    def view_assigned_orders(self,delivery_email):
        return self.delivery_repo.get_assigned_orders(delivery_email)
    
   