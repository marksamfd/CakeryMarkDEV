from app.models import Notification
from app.db import db
from firebase_admin import messaging
from app.models import CustomerUser


class Observer:
    def update(self, customer_email, message):
        raise NotImplementedError("not implemented")


class PushNotificationObserver(Observer):
    def update(self, customer_email, message):
        # Simulate sending a push notification
        print(f"Push Notification Sent to {customer_email}: {message}")


class DatabaseNotificationObserver(Observer):
    def update(self, customer_email, message):
        try:
            notification = Notification(
                customer_email=customer_email, message=message)
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            print(f"Error saving notification to database: {e}")


class OrderStatusNotifier:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, customer_email, message):
        for observer in self.observers:
            observer.update(customer_email, message)


# -------- push notification observer --------
class FirebaseNotificationObserver(Observer):
    def update(self, customer_email, message):
        try:
            token = self.get_customer_fcm_token(customer_email)
            if not token:
                print(f"Notoken for customer: {customer_email}")
                return

            # --- setting the message ---
            firebase_message = messaging.Message(
                notification=messaging.Notification(
                    title="Order Update",
                    body=message
                ),
                token=token
            )

            # --- send the message
            response = messaging.send(firebase_message)
            print(f"Successfully sent notification to {customer_email}: {response}")

        except Exception as e:
            print(f"Error sending Firebase notification: {e}")

    def get_customer_fcm_token(self, customer_email):
        """Fetch the the firebase token from the database"""
        customer = CustomerUser.query.filter_by(customeremail=customer_email).first()
        return customer.fcm_token if customer and customer.fcm_token else None