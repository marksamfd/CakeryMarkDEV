import random
from datetime import datetime, timedelta, timezone
from app.models import OTP
from app.db import db

class OTPService:
    def generate_and_save_otp(self, customer_email):
        otp_code = f"{random.randint(100000, 999999)}"
        expiry_time = datetime.now(timezone.utc) + timedelta(minutes=10)
        try:
            otp_entry = OTP(customer_email=customer_email, otp_code=otp_code, expiry_time=expiry_time)
            db.session.add(otp_entry)
            db.session.commit()
            return otp_code
        except Exception as e:
            db.session.rollback()
            print(f"(otp_service) error generating and saving the otp, error: {e}")
            return None
