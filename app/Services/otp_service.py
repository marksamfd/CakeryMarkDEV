from app.utils.otp_generator import OTPGenerator
from app.Repositories.otp_repository import OTPRepository
from app.Repositories.order_repository import OrderRepository
from datetime import datetime, timezone



class OTPService:
    def __init__(self, notifier):
        self.otp_generator = OTPGenerator()
        self.otp_repo = OTPRepository()
        self.order_repo = OrderRepository()
        self.notifier = notifier

    def generate_and_save_otp(self, customer_email, order_id):

        try:
            otp_code = self.otp_generator.generate_otp()
            expiry_time = self.otp_generator.get_expiry_time()

            otp_entry = self.otp_repo.save_otp(customer_email, otp_code, expiry_time, order_id)
            if otp_entry:
                self.notifier.notify_observers(
                    customer_email,
                    f"Your OTP code is {otp_code}. It will expire in 20 minutes. Please use it to confirm your order.",
                )
                return otp_code
            return None
        except Exception as e:
            print(f"(OTPService) Error generating and saving OTP: {e}")
            return None


    def validate_otp(self, customer_email, otp_code):
        try:
            # --------------- otp check ----------------
            otp_entry = self.otp_repo.get_otp(customer_email, otp_code)
            if not otp_entry:
                return {"error": "Invalid OTP"}, 400
            
            if otp_entry.expiry_time < datetime.now().replace(tzinfo=None):
                return {"error": "OTP expired"}, 400

            # ----------- get order to close ------------
            order_id = otp_entry.order_id
            if not order_id:
                return {"error": "Order ID not linked to OTP"}, 400
        
            result = self.order_repo.close_order(order_id)
            self.otp_repo.mark_otp_used(otp_entry)

            if "error" in result:
                return result, 400

            # Send notification
            message = "Your order has been confirmed successfully. Thank you for shopping with us!"
            self.notifier.notify_observers(customer_email, message)

            return {"message": "OTP validated successfully"}, 200
        except Exception as e:
            print(f"(OTPService) Error validating OTP: {e}")
            return {"error": "Error validating OTP"}, 500