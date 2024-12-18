from app.models import Notification
from app.db import db


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
            notification = Notification(customer_email=customer_email, message=message)
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
