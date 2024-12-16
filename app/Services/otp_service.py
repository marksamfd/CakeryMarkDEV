from app.utils.otp_generator import OTPGenerator
from app.Repositories.otp_repository import OTPRepository
from datetime import datetime, timezone

class OTPService:
    def __init__(self, notifier):
        self.otp_generator = OTPGenerator()
        self.otp_repo = OTPRepository()
        self.notifier = notifier

    def generate_and_save_otp(self, customer_email):
        try:
            otp_code = self.otp_generator.generate_otp()
            expiry_time = self.otp_generator.get_expiry_time()

            otp_entry = self.otp_repo.save_otp(customer_email, otp_code, expiry_time)
            if otp_entry:
                self.notifier.notify_observers(
                    customer_email,
                    f"Your OTP code is {otp_code}. It will expire in 20 minutes, please use it to confirm your order."
                )
                return otp_code
            return None
        except Exception as e:
            print(f"(OTPService) Error generating and saving OTP: {e}")
            return None
    def validate_otp(self, customer_email, otp_code):
        try:
            otp_entry = self.otp_repo.get_otp(customer_email, otp_code)

            if not otp_entry:
                return {"error": "Invalid OTP"}, 400
            
            # delted time zone to be able to compare with the normal time stamp from db
            if otp_entry.expiry_time < datetime.now().replace(tzinfo=None):
                return {"error": "OTP expired"}, 400

            # self.otp_repo.mark_otp_used(otp_entry) # mark otp as used
            message = "Your order has been confirmed successfully, thank you for shopping with us."
            self.notifier.notify_observers(customer_email, message) # send notification to customer to tell him that ORDER IS CLOSED
            return {"message": "OTP validated successfully"}, 200
        except Exception as e:
            print(f"(OTPService) Error validating OTP: {e}")
            return {"error": "Error validating OTP"}, 500
