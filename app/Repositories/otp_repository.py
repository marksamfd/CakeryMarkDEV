from app.models import OTP
from app.db import db
from datetime import datetime, timezone


class OTPRepository:
    # ------------------------- save otp to database ------------------------- (WILL BE UPDATED TO ENCRYPT)
    def save_otp(self, customer_email, otp_code, expiry_time, order_id):
        try:
            otp_entry = OTP(
                customer_email=customer_email,
                otp_code=otp_code,
                expiry_time=expiry_time,
                order_id=order_id,
            )
            db.session.add(otp_entry)
            

            db.session.commit()
            return otp_entry
        except Exception as e:
            db.session.rollback()
            print(f"(OTPRepository) Error saving OTP: {e}")
            return None


    # ------------------------- get otp from database -------------------------
    def get_otp(self, customer_email, otp_code):
        try:
            return OTP.query.filter_by(
                customer_email=customer_email, otp_code=str(otp_code)
            ).first()
        except Exception as e:
            print(f"(OTPRepository) Error fetching OTP: {e}")
            return None

    def mark_otp_used(self, otp_entry):
        try:
            otp_entry.is_used = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"(OTPRepository) Error marking OTP as used: {e}")

