from app.models import Notification
from app.db import db


class NotificationRepository:
    def save_notification(self, customer_email, message):
        try:
            new_notification = Notification(
                customer_email=customer_email, message=message
            )
            db.session.add(new_notification)
            db.session.commit()
            return {"message": "notification saved"}
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error saving notification: {e}"}
