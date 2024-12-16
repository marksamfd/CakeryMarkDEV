import random
from datetime import datetime, timedelta

class OTPGenerator:
    def generate_otp(self):
        return "{:06d}".format(random.randint(0,999999))

    def get_expiry_time(self, minutes=5):
        return datetime.now() + timedelta(minutes=minutes)
